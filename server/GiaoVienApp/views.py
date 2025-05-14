from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse

from DBApp.models import Enrollment
from DBApp.serializers import EnrollmentSerializer

@csrf_exempt
def EnrollmentScoreAPI(request, class_id=0, student_id=0):
    if request.method == "GET":
        enrollment=Enrollment.objects.filter(class_field = id)
        enrollment_serializer = EnrollmentSerializer(enrollment,many=True)
        return JsonResponse(enrollment_serializer.data, safe=False)
    elif request.method == 'PUT':
        if class_id == 0 or student_id == 0:
            return JsonResponse("Thiếu class_id hoặc student_id trong URL!", safe=False)
        try:
            enrollment = Enrollment.objects.get(class_field_id=class_id, student_id=student_id)
            enrollment_data = JSONParser().parse(request)

            serializer = EnrollmentSerializer(enrollment, data=enrollment_data, partial=True)  # partial=True allows partial updates

            if serializer.is_valid():
                serializer.save()
                return JsonResponse("Cập nhật điểm thành công!", safe=False)
            else:
                return JsonResponse({"error": "Dữ liệu không hợp lệ", "details": serializer.errors}, status=400)
        except Enrollment.DoesNotExist:
            return JsonResponse("Không tìm thấy học sinh trong lớp!", safe=False)
