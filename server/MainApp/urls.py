from django.urls import re_path
from MainApp import views
from . import controllers

urlpatterns = [
    # Login, register, logout
    re_path(r'^api/auth/login$', controllers.authAPI.LoginController.as_view()),
    re_path(r'^api/auth/register$',views.userRegisterAPI),
    re_path(r'^api/auth/forgot-password$',views.forgotPassword),
    re_path(r'^api/auth/me$', controllers.authAPI.SessionController.as_view()),
    re_path(r'^api/auth/logout$', controllers.authAPI.LogoutController.as_view()),

    # Student CRUD
    re_path(r'^api/students$', controllers.studentAPI.StudentController.as_view()),
    re_path(r'^api/students/(?P<sid>\d+)$', controllers.studentAPI.StudentController.as_view()),

    # Teacher CRUD
    re_path(r'^api/teachers$', controllers.teacherAPI.TeacherController.as_view()),
    re_path(r'^api/teachers/(?P<tid>\d+)$', controllers.teacherAPI.TeacherController.as_view()),

    # Class CRUD
    re_path(r'^api/classes$', controllers.classAPI.ClassController.as_view()),
    re_path(r'^api/classes/(?P<cid>\d+)$', controllers.classAPI.ClassController.as_view()),

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

    re_path(r'^api/student/(?P<sid>\d+)/grades$', views.getGradeStudent),

    re_path(r'^api/student/(?P<sid>\d+)/schedule$', views.ClassTimetableAPI),

    re_path(r'^api/dashboard/admin$', views.getSummaryAdmin),

    re_path(r'^api/messages$', views.MessageAPI),
    re_path(r'^api/messages/usr1/(?P<user1_id>\d+)/usr2/(?P<user2_id>\d+)$', views.MessageAPI),

    re_path(r'^api/registrations/(?P<cid>\d+)/student/(?P<sid>\d+)$', views.registrationAPI),

    re_path(r'^api/registrations/registered/(?P<sid>\d+)$', views.getRegistrated),

    re_path(r'^api/classes/(?P<class_id>\d+)/students/(?P<student_id>\d+)/grades$', views.EnrollmentScoreAPI),

    re_path(r'^api/classes/(?P<cid>\d+)/attendance$', views.AttendanceRecordAPI),
    re_path(r'^api/classes/(?P<cid>\d+)/students/(?P<sid>\d+)/attendance$', views.AttendanceRecordAPI),

    re_path(r'^api/classes/(?P<cid>\d+)/send-attendance$', views.sendAttendance),

    re_path(r'^api/classes/(?P<cid>\d+)/statistics$', views.getClassStats),

    re_path(r'^api/classes/(?P<cid>\d+)/details$', views.getMoreDetails),

    re_path(r'^api/dashboard/teacher/(?P<tid>\d+)$', views.getSummaryTeacher),

    re_path(r'^api/classes/(?P<cid>\d+)/student/(?P<sid>\d+)/work/(?P<aid>\d+)$', views.gradeWorkAPI),

    re_path(r'^api/classes/(?P<cid>\d+)/student/(?P<sid>\d+)/assignment/(?P<aid>\d+)$', views.submitWork),

    re_path(r'^api/dashboard/student/(?P<sid>\d+)$', views.getSummaryStudent)

    # re_path(r'^api/users', views.addUserAdmin),
    # re_path(r'^api/addAdmin', views.addAdmin)
]