from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse

from Login.models import Userlogin
from Login.serializers import UserloginSerializer

# Create your views here.
@csrf_exempt
def userLoginAPI(request):
    if request.method == 'GET': 
        users = Userlogin.objects.all()
        users_serializer = UserloginSerializer(users, many=True)
        return JsonResponse(users_serializer.data, safe=False)