from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse

from django.utils import timezone

from GiaoVienApp.models import Attendance
from GiaoVienApp.serializers import AttendanceSerializer

from DBApp.models import Enrollment, Class
from DBApp.serializers import EnrollmentSerializer

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