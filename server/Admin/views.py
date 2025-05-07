from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse

from DBApp.models import Class
from DBApp.serializers import ClassSerializer

from DBApp.models import Student
from DBApp.serializers import StudentSerializer
# Create your views here.

@csrf_exempt
def studentAPI(request,id=0):
    if request.method == 'GET':
        students = Student.objects.all()
        students_serializer = StudentSerializer(students,many=True)
        return JsonResponse(students_serializer.data, safe=False)
    elif request.method == 'DELETE':
        students=Student.objects.get(id=id)
        students.delete()
        return JsonResponse("Deleted Successfully!",safe=False)
    
@csrf_exempt
def classAPI(request,id=0):
    if request.method == 'GET':
        classes=Class.objects.all()
        classes_serializer = ClassSerializer(classes,many=True)
        return JsonResponse(classes_serializer.data, safe=False)
    elif request.method == 'POST':
        classes_data=JSONParser().parse(request)
        classes_serializer=ClassSerializer(data=classes_data)
        if classes_serializer.is_valid():
            classes_serializer.save()
            return JsonResponse("Thêm lớp vào cơ sở dữ liệu thành công!",safe=False)
        return JsonResponse("Nhập thiếu trường thông tin, vui lòng nhập lại!",safe=False)
    elif request.method == 'PUT':
        classes_data=JSONParser().parse(request)
        classes=Class.objects.get(EmployeeID = classes_data['class_id'])
        classes_serializer = ClassSerializer(classes, data=classes_data)
        if classes_serializer.is_valid():
            classes_serializer.save()
            return JsonResponse("Cập nhật thông tin thành công!", safe=False)
        return JsonResponse("Lỗi không cập nhật được thông tin!", safe=False)
    elif request.method == 'DELETE':
        classes=Class.objects.get(ClassID=id)
        classes.delete()
        return JsonResponse("Xóa lớp thành công!",safe=False)