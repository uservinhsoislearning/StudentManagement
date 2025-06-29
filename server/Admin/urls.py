from django.urls import re_path
from Admin import views

urlpatterns = [
    re_path(r'^api/students$', views.studentAPI),
    re_path(r'^api/students/([0-9]+)$', views.studentAPI),

    re_path(r'^api/classes$', views.classAPI),
    re_path(r'^api/classes/([0-9]+)$', views.classAPI),

    re_path(r'^api/teachers$', views.teacherAPI),
    re_path(r'^api/teachers/(?P<tid>\d+)$', views.teacherAPI),

    re_path(r'^api/classes/students$', views.EnrollmentAPI),
    re_path(r'^api/classes/(?P<class_id>\d+)/students$', views.EnrollmentAPI),
    re_path(r'^api/classes/(?P<class_id>\d+)/students/(?P<student_id>\d+)$', views.EnrollmentAPI),

    re_path(r'^api/classes/(?P<cid>\d+)/grades$', views.getGradeClass),

    re_path(r'^api/classes/([0-9]+)/get-students$', views.getStudentInClass),

    re_path(r'^api/classes/([0-9]+)/assignments$', views.AssignmentAPI),
    re_path(r'^api/classes/([0-9]+)/assignments-file$', views.AssignmentFileAPI),

    re_path(r'^api/course-classes$', views.CourseAPI),
    re_path(r'^api/course-classes/(?P<crid>\d+)$', views.CourseAPI),

    re_path(r'^api/course-classes-both$', views.CourseAndClass),
            
    re_path(r'^api/course-classes/import$', views.CSVUploadCourse),

    re_path(r'^api/reports$', views.ReportAPI),

    re_path(r'^api/semesters$', views.SemesterAPI),
    re_path(r'^api/semesters/([0-9]+)$', views.SemesterAPI),
    re_path(r'^api/semesters/([0-9]+)/toggle-status$', views.SemesterPatchAPI),

    re_path(r'^api/parents$', views.ParentAPI),
    re_path(r'^api/parents/(?P<pid>\d+)$', views.ParentAPI),

    re_path(r'^api/student/(?P<sid>\d+)/grades$', views.getGradeStudent),

    re_path(r'^api/student/(?P<sid>\d+)/schedule$', views.ClassTimetableAPI),

    re_path(r'^api/dashboard/admin$', views.getSummaryAdmin),

    re_path(r'^api/messages$', views.MessageAPI),
    re_path(r'^api/messages/usr1/(?P<user1_id>\d+)/usr2/(?P<user2_id>\d+)$', views.MessageAPI),

    re_path(r'^api/registrations/(?P<cid>\d+)/student/(?P<sid>\d+)$', views.registrationAPI),

    re_path(r'^api/registrations/registered/(?P<sid>\d+)$', views.getRegistrated)
]