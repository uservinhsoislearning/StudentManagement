from django.urls import re_path
from GiaoVienApp import views

urlpatterns = [
    re_path(r'^api/classes/(?P<class_id>\d+)/students/(?P<student_id>\d+)/grades$', views.EnrollmentScoreAPI),

    re_path(r'^api/classes/(?P<cid>\d+)/attendance$', views.AttendanceRecordAPI),
    re_path(r'^api/classes/(?P<cid>\d+)/students/(?P<sid>\d+)/attendance$', views.AttendanceRecordAPI),

    re_path(r'^api/classes/(?P<cid>\d+)/send-attendance$', views.sendAttendance),

    re_path(r'^api/classes/(?P<cid>\d+)/statistics$', views.getClassStats),

    re_path(r'^api/classes/(?P<cid>\d+)/details$', views.getMoreDetails),

    re_path(r'^api/dashboard/teacher/(?P<cid>\d+)$', views.getSummaryTeacher)
]