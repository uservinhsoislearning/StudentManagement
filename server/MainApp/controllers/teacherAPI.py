from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from MainApp.models import Teacher
from MainApp.serializers import TeacherSerializer, TeacherWithIDSerializer

class TeacherController(APIView):
    def get(self, request):
        teachers = Teacher.objects.all()
        teachers_serializer = TeacherWithIDSerializer(teachers,many=True)
        return Response(teachers_serializer.data)
    
    def post(self, request):
        teachers_serializer = TeacherSerializer(data=request.data)
        if teachers_serializer.is_valid():
            teachers_serializer.save()
            return Response("Thêm thầy/cô vào cơ sở dữ liệu thành công!", status=status.HTTP_201_CREATED)
        return Response(teachers_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, tid):
        teachers = Teacher.objects.get(teacher_id = tid)
        teachers_serializer = TeacherSerializer(teachers, data=request.data)
        if teachers_serializer.is_valid():
            teachers_serializer.save()
            return Response("Cập nhật thông tin thành công!")
        return Response("Lỗi không cập nhật được thông tin!", status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, tid):
        try:
            teachers = Teacher.objects.get(teacher_id=tid)
            teachers.delete()
            return Response("Xóa thầy/cô thành công!")
        except Teacher.DoesNotExist:
            return Response("Không tìm thấy thầy/cô!", status=status.HTTP_404_NOT_FOUND)