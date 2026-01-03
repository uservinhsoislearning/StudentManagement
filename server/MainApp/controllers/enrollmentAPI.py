from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.db.models import F, ExpressionWrapper, DurationField
from django.db.models.functions import Now, Extract

from MainApp.models import Enrollment, Attendance, Class
from MainApp.serializers import EnrollmentSerializer, EnrollmentGradeSerializer, StudentWithIDSerializer, AttendanceSerializer

class EnrollmentController(APIView):
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
    # ... [Logic] ...
    pass

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

class ClassStatsController(APIView):
    # ... [Logic] ...
    pass

class RegistrationController(APIView):
    # ... [Logic] ...
    pass