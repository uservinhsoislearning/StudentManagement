from django.urls import re_path
from GiaoVienApp import views

urlpatterns = [
    re_path(r'^api/classes/(?P<class_id>\d+)/students/(?P<student_id>\d+)/score$', views.EnrollmentScoreAPI),

    re_path(r'^api/classes/(?P<class_id>\d+)/attendance$', views.AttendanceRecordAPI)
]