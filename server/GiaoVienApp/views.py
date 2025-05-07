from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth.hashers import check_password
from django.utils.crypto import get_random_string
from django.core.mail import send_mail

from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse

from DBApp.models import Class
from Login.serializers import UserloginSerializer

# Create your views here.
