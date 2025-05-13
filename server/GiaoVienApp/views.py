from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth.hashers import check_password
from django.utils.crypto import get_random_string
from django.core.mail import send_mail

from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse

from DBApp.models import Assignment
from DBApp.serializers import AssignmentSerializer

# Create your views here.
# @csrf_exempt
# def AssignmentAPI(request, id=0):
#     if request.method == 'GET':
#         assignments=Assignment.objects.filter(class_field = id)
#         assignments_serializer = AssignmentSerializer(assignments,many=True)
#         return JsonResponse(assignments_serializer.data, safe=False)
#     elif request.method == 'POST':
#         assignments_data=JSONParser().parse(request)
#         assignments_data['class_field'] = id
#         assignments_serializer=AssignmentSerializer(data=assignments_data)
#         if assignments_serializer.is_valid():
#             assignments_serializer.save()
#             return JsonResponse("Thêm bài tập thành công!",safe=False)
#         return JsonResponse("Nhập thiếu trường thông tin, vui lòng nhập lại!",safe=False)
#     elif request.method == 'PUT':
#         assignments_data=JSONParser().parse(request)
#         assignments=Assignment.objects.get(assignment_id = assignments_data['assignment_id'])
#         try:
#             assignments_serializer = AssignmentSerializer(assignments, data=assignments_data,class_field = id)
#         except Assignment.DoesNotExist:
#             return JsonResponse("Không tìm thấy bài tập cho lớp này!", safe=False)
#         if assignments_serializer.is_valid():
#             assignments_serializer.save()
#             return JsonResponse("Cập nhật bài tập thành công!", safe=False)
#         return JsonResponse("Lỗi không cập nhật được bài tập!", safe=False)
#     elif request.method == 'DELETE':
#         assignments=Assignment.objects.get(class_id=id)
#         assignments.delete()
#         return JsonResponse("Xóa bài tập thành công!",safe=False)