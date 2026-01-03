from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from MainApp.models import Enrollment
from MainApp.serializers import EnrollmentSerializer, EnrollmentGradeSerializer, StudentWithIDSerializer

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

class AttendanceRecordController(APIView):
    # ... [Logic] ...
    pass

class SendAttendanceController(APIView):
    # ... [Logic] ...
    pass

class EnrollmentScoreController(APIView):
    def get(request, cid):
        try:
            enrollment = Enrollment.objects.filter(class_field = cid)
            enrollment_serializer = EnrollmentGradeSerializer(enrollment,many=True)
            return Response(enrollment_serializer.data)
        except Enrollment.DoesNotExist:
            return Response("Không tìm thấy điểm trong lớp!", status=status.HTTP_404_NOT_FOUND)
        
    def post(request, cid):
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