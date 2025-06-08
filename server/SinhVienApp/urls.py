from django.urls import re_path
from SinhVienApp import views

urlpatterns = [
    re_path(r'^api/classes/(?P<cid>\d+)/student/(?P<sid>\d+)/work/(?P<aid>\d+)$', views.submitWork),

    re_path(r'^api/dashboard/student/(?P<sid>\d+)$', views.getSummaryStudent),

    re_path(r'^api/dashboard/parent/(?P<pid>\d+)$', views.getSummaryParent)
]