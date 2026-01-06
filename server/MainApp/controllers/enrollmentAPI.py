from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.core.mail import EmailMultiAlternatives
from django.db.models import F, ExpressionWrapper, DurationField, Avg, Max, Min
from django.db.models.functions import Now, Extract
from django.template.loader import render_to_string
import server.settings as settings

from MainApp.models import Enrollment, Attendance, Class, Student
from MainApp.serializers import EnrollmentSerializer, EnrollmentGradeSerializer, StudentWithIDSerializer, AttendanceSerializer

class EnrollmentController(APIView):
    def get(self, request, sid):
        try:
            # Get all registrations for the student
            enrollments = Enrollment.objects.filter(student_id=sid).select_related('class_field')
            class_names = [reg.class_field.class_name for reg in enrollments if reg.class_field]
            return Response({'registered_classes': class_names})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def post(self, request):
        enrollment_data = request.data
        enrollment_data['withdrawal_date'] = None 
        enrollment_data['grade'] = None
        enrollment_data['midterm'] = None
        enrollment_data['final'] = None

        enrollment_serializer = EnrollmentSerializer(data=enrollment_data)
        if enrollment_serializer.is_valid():
            enrollment_serializer.save()
            return Response("Thêm học sinh vào lớp thành công!", status=status.HTTP_201_CREATED)
        return Response("Xin thử lại!", status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, cid, sid):
        if not cid or not sid:
            return Response("Thiếu class_id hoặc student_id trong URL!", status=status.HTTP_400_BAD_REQUEST)

        try:
            enrollment = Enrollment.objects.get(class_field_id=cid, student_id=sid)
        except Enrollment.DoesNotExist:
            return Response("Không tìm thấy học sinh trong lớp!", status=status.HTTP_404_NOT_FOUND)

        # Allow partial update for grade fields
        enrollment.grade = request.data.get('grade', enrollment.grade)
        enrollment.midterm = request.data.get('midterm', enrollment.midterm)
        enrollment.final = request.data.get('final', enrollment.final)
        enrollment.save()

        serializer = EnrollmentSerializer(enrollment)
        return Response(serializer.data)
    
    def delete(self, request, cid, sid):
        if not cid or not sid:
            return Response("Thiếu class_id hoặc student_id trong URL!", status=status.HTTP_400_BAD_REQUEST)

        try:
            enrollment = Enrollment.objects.get(class_field_id=cid, student_id=sid)
            enrollment.delete()
            return Response("Xóa học sinh khỏi lớp thành công!", status=status.HTTP_200_OK)
        except Enrollment.DoesNotExist:
            return Response("Không tìm thấy học sinh trong lớp!", status=status.HTTP_404_NOT_FOUND)

class AttendanceController(APIView):
    def get(self, request, cid):
        closest = (
            Attendance.objects.filter(class_field_id=cid)
            .annotate(
                time_diff=ExpressionWrapper(
                    Now() - F('timestamp'),
                    output_field=DurationField()
                )
            )
            .annotate(
                seconds_diff=Extract(F('time_diff'), 'epoch')
            )
            .order_by('seconds_diff')
            .values('timestamp__date')
            .first()
        )

        if not closest:
            return Response([])

        closest_date = closest['timestamp__date']
        attendance = Attendance.objects.filter(class_field_id=cid, timestamp__date=closest_date)
        attendance_serializer = AttendanceSerializer(attendance, many=True)
        return Response(attendance_serializer.data)

    def post(self, request, cid):
        try:
            if not Class.objects.filter(class_id=cid).exists():
                return Response("Lớp không tồn tại!", status=status.HTTP_404_NOT_FOUND)

            enrollments = Enrollment.objects.filter(class_field_id=cid)
            if not enrollments.exists():
                return Response("Không có học sinh nào trong lớp này!", status=status.HTTP_404_NOT_FOUND)

            created_records = []
            for enrollment in enrollments:
                attendance = Attendance.objects.create(
                    class_field_id=cid,
                    student=enrollment.student_id
                )
                created_records.append(attendance)

            serializer = AttendanceSerializer(created_records, many=True)
            return Response("Tạo điểm danh thành công!")

        except Exception as e:
            return Response({"error": str(e)}, status=500)

    def patch(self, request, cid, sid):
        try:
            closest = (
                Attendance.objects.filter(class_field_id=cid, student=sid)
                .annotate(
                    time_diff=ExpressionWrapper(
                        Now() - F('timestamp'),
                        output_field=DurationField()
                    )
                )
                .annotate(
                    seconds_diff=Extract(F('time_diff'), 'epoch')
                )
                .order_by('seconds_diff')
                .first()
            )

            if not closest:
                return Response("Không có bản ghi điểm danh!", status=status.HTTP_404_NOT_FOUND)

            closest.is_present = not closest.is_present
            closest.save()

            return Response({"message": "Student marked as present."}) if closest.is_present else Response({"message": "Student marked as NOT present."})

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class SendAttendanceController(APIView):
    def post(self, request, cid):
        try:
            closest = (
                Attendance.objects.filter(class_field_id=cid)
                .annotate(
                    time_diff=ExpressionWrapper(
                        Now() - F('timestamp'),
                        output_field=DurationField()
                    )
                )
                .annotate(
                    seconds_diff=Extract(F('time_diff'), 'epoch')
                )
                .order_by('seconds_diff')
                .values('timestamp__date')
                .first()
            )

            if not closest:
                return Response("Không có bản ghi điểm danh nào để gửi!", status=status.HTTP_404_NOT_FOUND)

            closest_date = closest['timestamp__date']

            absent_records = Attendance.objects.filter(
                class_field_id=cid,
                timestamp__date=closest_date,
                is_present=False
            )

            if not absent_records.exists():
                return Response("Không có học sinh nào vắng vào ngày gần nhất!")

            emails_sent = []
            class_data = Class.objects.get(class_id=cid)
            teacher = class_data.class_teacher

            for record in absent_records:
                try:
                    sid = record.student
                    student = Student.objects.get(student_id=sid)
                    parent_email = student.parent_email
                    if not parent_email:
                        print(f"Skipping student {student.student_name}: No parent_email found.")
                        continue
                    subject = "Thông báo vắng mặt"

                    html_message = render_to_string('absent.html', {
                        'student_name': student.student_name,
                        'class_name': class_data.class_name,
                        'date': closest_date,
                        'teacher_email': teacher.teacher_email
                    })

                    plain_message = (
                        f"Học sinh {student.student_name} đã vắng mặt buổi học vào ngày {closest_date}, "
                        f"lớp {class_data.class_name}. Email liên hệ giáo viên: {teacher.teacher_email}"
                    )

                    from_email = settings.EMAIL_HOST_USER

                    email = EmailMultiAlternatives(subject, plain_message, from_email, parent_email)
                    email.attach_alternative(html_message, "text/html")
                    email.send()
                    emails_sent.append(parent_email) # for debugging

                except Exception as e:
                    print(f"Error processing student ID {record.student}: {e}")
                    continue

            return Response({ # for debugging
                "message": "Email đã được gửi đến phụ huynh học sinh vắng mặt!",
                "recipients": emails_sent
            })

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class EnrollmentScoreController(APIView):
    def get(self, request, cid):
        try:
            enrollment = Enrollment.objects.filter(class_field = cid)
            enrollment_serializer = EnrollmentGradeSerializer(enrollment,many=True)
            return Response(enrollment_serializer.data)
        except Enrollment.DoesNotExist:
            return Response("Không tìm thấy điểm trong lớp!", status=status.HTTP_404_NOT_FOUND)
        
    def post(self, request, cid):
        try:
            enrollment = Enrollment.objects.filter(class_field_id = cid)
            students = [cs.student for cs in enrollment]
            students_serializer = StudentWithIDSerializer(students, many=True)
            return Response(students_serializer.data)
        except Enrollment.DoesNotExist:
            return Response("Không tìm được lớp!", status=status.HTTP_404_NOT_FOUND)
        
    def put(self, request, cid, sid):
        if not cid or not sid:
            return Response("Thiếu class_id hoặc student_id trong URL!", status=status.HTTP_400_BAD_REQUEST)
        try:
            enrollment = Enrollment.objects.get(class_field_id=cid, student_id=sid)
            enrollment_data = request.data

            serializer = EnrollmentSerializer(enrollment, data=enrollment_data, partial=True)  # partial=True allows partial updates

            if serializer.is_valid():
                serializer.save()
                return Response("Cập nhật điểm thành công!")
            else:
                return Response("Dữ liệu không hợp lệ!", status=status.HTTP_400_BAD_REQUEST)
        except Enrollment.DoesNotExist:
            return Response("Không tìm thấy học sinh trong lớp!", status=status.HTTP_404_NOT_FOUND)

class ClassStatsController(APIView):
    def get(self, request, cid):
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

        return Response(data=grade_data)