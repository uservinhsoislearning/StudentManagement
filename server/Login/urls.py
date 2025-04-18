from django.urls import re_path
from Login import views

urlpatterns = [
    re_path(r'^api/auth/login$', views.userLoginAPI)
]