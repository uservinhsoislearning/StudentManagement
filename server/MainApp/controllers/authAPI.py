from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import check_password
from django.template.loader import render_to_string
from django.utils.crypto import get_random_string
from django.core.mail import EmailMultiAlternatives
import server.settings as settings
from MainApp import models as m
from MainApp import serializers as s

class UserLoginController(APIView):
    def post(self, request):
        # ... [Paste UserLoginController logic here] ...
        pass

class UserRegisterController(APIView):
    def post(self, request):
        # ... [Paste UserRegisterController logic here] ...
        pass

class CurrentUserController(APIView):
    def get(self, request):
        # ... [Paste CurrentUserController logic here] ...
        pass

class UserLogoutController(APIView):
    def post(self, request):
        request.session.flush()
        return Response("Logged out successfully!")

class ForgotPasswordController(APIView):
    def post(self, request):
        # ... [Paste logic] ...
        pass