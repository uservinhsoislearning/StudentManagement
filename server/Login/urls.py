from django.urls import re_path
from Login import views

urlpatterns = [
    re_path(r'^api/auth/login$', views.userLoginAPI),
    re_path(r'^api/auth/register$',views.userRegisterAPI),
    re_path(r'^api/auth/forgot-password$',views.forgotPassword),
    re_path(r'^api/auth/me$', views.getCurrentUser),
    re_path(r'^api/auth/logout$', views.userLogout)
]