from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse

from DBApp.models import Class,Teacher,Student
from DBApp.serializers import ClassSerializer,TeacherSerializer,StudentSerializer
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
        classes=Class.objects.get(class_id = classes_data['class_id'])
        classes_serializer = ClassSerializer(classes, data=classes_data)
        if classes_serializer.is_valid():
            classes_serializer.save()
            return JsonResponse("Cập nhật thông tin thành công!", safe=False)
        return JsonResponse("Lỗi không cập nhật được thông tin!", safe=False)
    elif request.method == 'DELETE':
        classes=Class.objects.get(class_id=id)
        classes.delete()
        return JsonResponse("Xóa lớp thành công!",safe=False)
    
@csrf_exempt
def teacherAPI(request,id=0):
    if request.method == 'GET':
        teachers=Teacher.objects.all()
        teachers_serializer = TeacherSerializer(teachers,many=True)
        return JsonResponse(teachers_serializer.data, safe=False)
    elif request.method == 'POST':
        teachers_data=JSONParser().parse(request)
        teachers_serializer=TeacherSerializer(data=teachers_data)
        if teachers_serializer.is_valid():
            teachers_serializer.save()
            return JsonResponse("Thêm thầy/cô vào cơ sở dữ liệu thành công!",safe=False)
        return JsonResponse("Nhập thiếu trường thông tin, vui lòng nhập lại!",safe=False)
    elif request.method == 'PUT':
        teachers_data=JSONParser().parse(request)
        teachers=Teacher.objects.get(teacher_id = teachers_data['teacher_id'])
        teachers_serializer = TeacherSerializer(teachers, data=teachers_data)
        if teachers_serializer.is_valid():
            teachers_serializer.save()
            return JsonResponse("Cập nhật thông tin thành công!", safe=False)
        return JsonResponse("Lỗi không cập nhật được thông tin!", safe=False)
    elif request.method == 'DELETE':
        teachers=Teacher.objects.get(class_id=id)
        teachers.delete()
        return JsonResponse("Xóa thầy/cô thành công!",safe=False)
    