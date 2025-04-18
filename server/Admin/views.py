from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
# from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse

from DBApp.models import Student
from Admin.serializers import StudentSerializer
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