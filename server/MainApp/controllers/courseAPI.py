from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from MainApp.models import Course
from MainApp.serializers import CourseSerializer, CourseWithIDSerializer

class CourseController(APIView):
    def get(self, request):
        courses = Course.objects.all()
        courses_serializer = CourseWithIDSerializer(courses,many=True)
        return Response(courses_serializer.data)
    
    def post(self, request):
        courses_data = request.data
        courses_serializer = CourseSerializer(data=courses_data)
        if courses_serializer.is_valid():
            courses_serializer.save()
            return Response("Thêm môn học thành công!", status=status.HTTP_201_CREATED)
        return Response(courses_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, crid):
        courses_data = request.data
        courses = Course.objects.get(course_id=crid)
        courses_serializer = CourseSerializer(courses, data=courses_data)
        if courses_serializer.is_valid():
            courses_serializer.save()
            return Response("Cập nhật thông tin môn học thành công!")
        return Response("Lỗi không cập nhật được thông tin!", status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, crid):
        courses = Course.objects.get(course_id=crid)
        courses.delete()
        return Response("Xóa môn học thành công!")