from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse

from django.db.models import Avg, Max, Min
from django.utils import timezone
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string

from GiaoVienApp.models import Attendance
from GiaoVienApp.serializers import AttendanceSerializer

from DBApp.models import Enrollment, Class, Student, Studentparent, Work
from DBApp.serializers import EnrollmentSerializer, WorkScoreSerializer

import server.settings as settings

@csrf_exempt
def EnrollmentScoreAPI(request, class_id=0, student_id=0):
    if request.method == "GET":
        enrollment=Enrollment.objects.filter(class_field = class_id)
        enrollment_serializer = EnrollmentSerializer(enrollment,many=True)
        return JsonResponse(enrollment_serializer.data, safe=False)
    elif request.method == 'PUT':
        if class_id == 0 or student_id == 0:
            return JsonResponse("Thiếu class_id hoặc student_id trong URL!", safe=False)
        try:
            enrollment = Enrollment.objects.get(class_field_id=class_id, student_id=student_id)
            enrollment_data = JSONParser().parse(request)

            serializer = EnrollmentSerializer(enrollment, data=enrollment_data, partial=True)  # partial=True allows partial updates

            if serializer.is_valid():
                serializer.save()
                return JsonResponse("Cập nhật điểm thành công!", safe=False)
            else:
                return JsonResponse({"error": "Dữ liệu không hợp lệ", "details": serializer.errors}, status=400)
        except Enrollment.DoesNotExist:
            return JsonResponse("Không tìm thấy học sinh trong lớp!", safe=False)

@csrf_exempt
def AttendanceRecordAPI(request, cid=0, sid=0):
    if request.method == 'GET':
        attendance=Attendance.objects.filter(class_field_id=cid,timestamp__date=timezone.now().date())
        attendance_serializer=AttendanceSerializer(attendance,many=True)
        return JsonResponse(attendance_serializer.data, safe=False)
    elif request.method == 'POST':
        try:
            # Validate class existence
            if not Class.objects.filter(class_id=cid).exists():
                return JsonResponse({"error": "Lớp không tồn tại!"}, status=404)

            # Get all enrollments for this class
            enrollments = Enrollment.objects.filter(class_field_id=cid)

            if not enrollments.exists():
                return JsonResponse({"error": "Không có học sinh nào trong lớp này!"}, status=404)

            # Create attendance records for each student
            created_records = []
            for enrollment in enrollments:
                attendance = Attendance.objects.create(
                    class_field_id=cid,
                    student=enrollment.student_id
                )
                created_records.append(attendance)

            serializer = AttendanceSerializer(created_records, many=True)
            return JsonResponse({"message": "Tạo điểm danh thành công!", "data": serializer.data}, safe=False)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    elif request.method == 'PATCH':
        try:
            record = Attendance.objects.get(student=sid, class_field_id=cid, timestamp__date=timezone.now().date())
            record.is_present = not record.is_present
            record.save()
            return JsonResponse({"message": "Student marked as present."}) if record.is_present == True else JsonResponse({"message": "Student marked as NOT present."})
        except Attendance.DoesNotExist:
            return JsonResponse({"error": "Attendance record not found."}, status=404)
        
@csrf_exempt
def sendAttendance(request, cid=0):
    if request.method == 'POST':
        try:
            today = timezone.now().date()

            # Get today's attendance records for the class where students are absent
            absent_records = Attendance.objects.filter(
                class_field_id=cid,
                timestamp__date=today,
                is_present=False
            )

            if not absent_records.exists():
                return JsonResponse("Không có học sinh nào vắng hôm nay!", safe=False)

            emails_sent = []

            for record in absent_records:
                try:
                    sid = record.student
                    student = Student.objects.get(student_id=sid)
                    dummy = Studentparent.objects.filter(student=sid)
                    class_data = Class.objects.get(class_id=cid)
                    teacher=class_data.class_teacher
                    for dum in dummy:
                        p = dum.parent
                        subject = "Thông báo vắng mặt"

                        html_message = render_to_string('absent.html', {
                            'student_name': student.student_name,
                            'class_name': class_data.class_name,
                            'date': today,
                            'teacher_email': teacher.teacher_email
                        })
                        plain_message = f"Học sinh {student.student_name} đã vắng mặt buổi học hôm nay ({today}), lớp {class_data.class_name}. Email liên hệ giáo viên: {teacher.teacher_email}"
                        from_email = settings.EMAIL_HOST_USER
                        to_email = [p.parent_email]

                        # Send email with HTML and plain fallback
                        email = EmailMultiAlternatives(subject, plain_message, from_email, to_email)
                        email.attach_alternative(html_message, "text/html")
                        email.send()
                        emails_sent.append(p.parent_email)
                except Exception as e:
                    print(f"Error processing {e}")
                    continue  

            return JsonResponse({"message": "Email đã được gửi đến phụ huynh học sinh vắng mặt!", "recipients": emails_sent})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
        
@csrf_exempt
def gradeWorkAPI(request,cid=0,sid=0,aid=0):
    if request.method == 'PUT':
        work_data = JSONParser().parse(request)
        work_serializer = WorkScoreSerializer(data={'score': work_data['score']}, partial=True)
        if work_serializer.is_valid():
            work_serializer.save()
            return JsonResponse(work_serializer.data, safe=False)
        return JsonResponse(work_serializer.errors, status=400)

    # DELETE request: delete the work entry
    elif request.method == 'DELETE':
        if cid == 0 or sid == 0 or aid == 0:
            return JsonResponse("Thiếu thông tin trong URL!", safe=False)
        try:
            work = Work.objects.get(class_field=cid, student=sid, assignment=aid)
            work.delete()
            return JsonResponse("Work entry deleted successfully", safe=False)
        except Work.DoesNotExist:
            return JsonResponse("Không có bài làm này!", safe=False)
        
@csrf_exempt
def getClassStats(request, cid=0):
    if request.method == 'GET':
        # Get all grades for this class
        class_enrollments = Enrollment.objects.filter(class_field_id=cid)

        # Compute statistics
        stats = class_enrollments.aggregate(
            maxScore=Max('grade'),
            minScore=Min('grade'),
            avgScore=Avg('grade')
        )

        # Build response
        grade_data = {
            'maxScore': stats['maxScore'],
            'minScore': stats['minScore'],
            'avgScore': round(stats['avgScore'], 2) if stats['avgScore'] is not None else None
        }

        return JsonResponse(data=grade_data, safe=False)