from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from MainApp import models as m
from MainApp import serializers as s

class StudentController(APIView):
    def get(self, request):
        students = m.Student.objects.all()
        students_serializer = s.StudentWithIDSerializer(students,many=True)
        return Response(students_serializer.data)
    
    def post(self, request):
        # students_data=JSONParser().parse(request)
        students_serializer = s.StudentSerializer(data=request.data)
        if students_serializer.is_valid():
            students_serializer.save()
            return Response("Thêm học sinh vào cơ sở dữ liệu thành công!", status=status.HTTP_201_CREATED)
        return Response(students_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, sid):
        # students_data=JSONParser().parse(request)
        students=m.Student.objects.get(student_id = sid)
        students_serializer = s.StudentSerializer(students, data=request.data)
        if students_serializer.is_valid():
            students_serializer.save()
            return Response("Cập nhật thông tin thành công!")
        return Response("Lỗi không cập nhật được thông tin!", status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, sid):
        try:
            students=m.Student.objects.get(student_id=sid)
            students.delete()
            return Response("Xóa học sinh thành công!")
        except m.Student.DoesNotExist:
            return Response("Không tìm thấy học sinh!", status=status.HTTP_404_NOT_FOUND)