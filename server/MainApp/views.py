from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse

from MainApp import models as m
from MainApp import serializers as s

# These APIs are kept for inserting Admin into the database (remember that admin cannot be created)
# @csrf_exempt
# def addAdmin(request):
#     if request.method == "POST":
#         admin_data=JSONParser().parse(request)
#         admin_serializer=s.AdminSerializer(data=admin_data)
#         if admin_serializer.is_valid():
#             admin_serializer.save()
#             return JsonResponse("Thêm admin vào cơ sở dữ liệu thành công!",safe=False)
#         return JsonResponse(admin_serializer.errors,safe=False)

# @csrf_exempt
# def addUserAdmin(request):
#     if request.method == "POST":
#         admin_data=JSONParser().parse(request)
#         admin_serializer=s.UserloginSerializer(data=admin_data)
#         if admin_serializer.is_valid():
#             admin_serializer.save()
#             return JsonResponse("Thêm user admin vào cơ sở dữ liệu thành công!",safe=False)
#         return JsonResponse(admin_serializer.errors,safe=False)