from django.urls import re_path
from Admin import views

# from django.conf.urls.static import static
# from django.conf import settings

urlpatterns = [
    re_path(r'^api/students$', views.studentAPI),
    re_path(r'^api/students/([0-9]+)$', views.studentAPI),

    re_path(r'^api/classes$', views.classAPI),
    re_path(r'^api/classes/([0-9]+)$', views.classAPI),

    re_path(r'^api/teachers$', views.teacherAPI),
    re_path(r'^api/teachers/([0-9]+)$', views.teacherAPI),

    re_path(r'^api/classes/students$', views.EnrollmentAPI),
    re_path(r'^api/classes/(?P<class_id>\d+)/students$', views.EnrollmentAPI),
    re_path(r'^api/classes/(?P<class_id>\d+)/students/(?P<student_id>\d+)$', views.EnrollmentAPI),

    re_path(r'^api/classes/([0-9]+)/get-students$', views.getStudentInClass),

    re_path(r'^api/classes/([0-9]+)/assignments$', views.AssignmentAPI),
    re_path(r'^api/classes/([0-9]+)/assignments$', views.AssignmentFileAPI),

    re_path(r'^api/course-classes$', views.CourseAPI),
    re_path(r'^api/course-classes/([0-9]+)$', views.CourseAPI),
            
    re_path(r'^api/course-classes/import$', views.CSVUploadCourse),

    re_path(r'^api/reports$', views.ReportAPI),

    re_path(r'^api/semesters$', views.SemesterAPI),
    re_path(r'^api/semesters/([0-9]+)$', views.SemesterAPI),
    re_path(r'^api/semesters/([0-9]+)/toggle-status$', views.SemesterPatchAPI)
]