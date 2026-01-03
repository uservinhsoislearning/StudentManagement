from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from MainApp.models import Class, Enrollment
from MainApp.serializers import ClassSerializer, ClassWithTimetableSerializer, ClassWithCourseSerializer

class ClassController(APIView):
    def get(self, request):
        classes = Class.objects.all()
        classes_serializer = ClassWithTimetableSerializer(classes,many=True)
        return Response(classes_serializer.data)
    
    def post(self, request):
        classes_serializer = ClassWithCourseSerializer(data=request.data)
        if classes_serializer.is_valid():
            classes_serializer.save()
            return Response("Thêm lớp vào cơ sở dữ liệu thành công!", status=status.HTTP_201_CREATED)
        return Response(classes_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, cid):
        classes = Class.objects.get(class_id = cid)
        classes_serializer = ClassSerializer(classes, data=request.data)
        if classes_serializer.is_valid():
            classes_serializer.save()
            return Response("Cập nhật thông tin thành công!")
        return Response("Lỗi không cập nhật được thông tin!", status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, cid):
        try:
            classes = Class.objects.get(class_id=cid)
            classes.delete()
            return Response("Xóa lớp thành công!")
        except Class.DoesNotExist:
            return Response("Không tìm thấy lớp!", status=status.HTTP_404_NOT_FOUND)
        
class TimetableController(APIView):
    def get(request, sid):
        class_ids = Enrollment.objects.filter(student_id=sid).values_list('class_field_id', flat=True)
        classes = Class.objects.filter(class_id__in=class_ids).prefetch_related('timetables')
        serializer = ClassWithTimetableSerializer(classes, many=True)
        return Response(serializer.data)