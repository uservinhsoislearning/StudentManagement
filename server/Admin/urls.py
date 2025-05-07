from django.urls import re_path
from Admin import views

# from django.conf.urls.static import static
# from django.conf import settings

urlpatterns = [
    re_path(r'^student$', views.studentAPI),
    re_path(r'^student/([0-9]+)$', views.studentAPI),

    re_path(r'^api/classes$', views.classAPI),
    re_path(r'^api/classes/([0-9]+)$', views.classAPI)
]