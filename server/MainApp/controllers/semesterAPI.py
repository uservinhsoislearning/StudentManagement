from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from MainApp.models import Semester
from MainApp.serializers import SemesterWithIDSerializer, SemesterSerializer
class SemesterController(APIView):
    def get(self, request):
        semesters = Semester.objects.all()
        semesters_serializer = SemesterWithIDSerializer(semesters, many=True)
        return Response(semesters_serializer.data)
    
    def post(self, request):
        semesters_data = request.data
        semesters_serializer = SemesterSerializer(data=semesters_data)
        if semesters_serializer.is_valid():
            semesters_serializer.save()
            return Response("Thêm học kỳ thành công!", status=status.HTTP_201_CREATED)
        return Response(semesters_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, sem_id):
        semesters_data = request.data
        semesters = Semester.objects.get(semester_id=sem_id)
        semesters_serializer = SemesterSerializer(semesters, data=semesters_data)
        if semesters_serializer.is_valid():
            semesters_serializer.save()
            return Response("Cập nhật thông tin thành công!")
        return Response(semesters_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, sem_id):
        semesters = Semester.objects.get(semester_id=sem_id)
        semesters.delete()
        return Response("Xóa học kỳ thành công!")
    
    def patch(self, request, sem_id):
        try:
            semesters = Semester.objects.get(semester_id=sem_id)
            semesters.isActive = not semesters.isActive
            semesters.save()
            return Response("Cập nhật trạng thái thành công!")
        except Semester.DoesNotExist:
            return Response("Không tìm thấy học kỳ!", status=status.HTTP_404_NOT_FOUND)