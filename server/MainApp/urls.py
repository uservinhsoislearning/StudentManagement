from django.urls import re_path
# from MainApp import views
from . import controllers

urlpatterns = [
    # Login, register, logout
    re_path(r'^api/auth/login$', controllers.authAPI.LoginController.as_view()),
    re_path(r'^api/auth/register$', controllers.authAPI.RegisterController.as_view()),
    re_path(r'^api/auth/forgot-password$',controllers.authAPI.ForgotPasswordController.as_view()),
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

    # Enrollment (Add student to a class)
    re_path(r'^api/classes/students$', controllers.enrollmentAPI.EnrollmentController.as_view()),
    re_path(r'^api/classes/(?P<cid>\d+)/students/(?P<sid>\d+)$', controllers.enrollmentAPI.EnrollmentController.as_view()),

    # Get all classes a student has registered
    re_path(r'^api/registrations/registered/(?P<sid>\d+)$', controllers.enrollmentAPI.EnrollmentController.as_view()),

    # Semester CRUD
    re_path(r'^api/semesters$', controllers.semesterAPI.SemesterController.as_view()),
    re_path(r'^api/semesters/(?P<sem_id>\d+)$', controllers.semesterAPI.SemesterController.as_view()),
    re_path(r'^api/semesters/(?P<sem_id>\d+)/toggle-status$', controllers.semesterAPI.SemesterController.as_view()),

    # Course CRUD
    re_path(r'^api/course-classes$', controllers.courseAPI.CourseController.as_view()),
    re_path(r'^api/course-classes/(?P<crid>\d+)$', controllers.courseAPI.CourseController.as_view()),
    re_path(r'^api/course-classes/import$', controllers.courseAPI.CourseFileController.as_view()),

    # Grade from student
    re_path(r'^api/classes/(?P<cid>\d+)/grades$', controllers.enrollmentAPI.EnrollmentScoreController.as_view()),
    re_path(r'^api/classes/(?P<cid>\d+)/get-students$', controllers.enrollmentAPI.EnrollmentScoreController.as_view()),

    # Lấy điểm chấm điểm học sinh trong lớp
    re_path(r'^api/classes/(?P<cid>\d+)/students/(?P<sid>\d+)/grades$', controllers.enrollmentAPI.EnrollmentScoreController.as_view()),

    # Assignment CRUD
    re_path(r'^api/classes/(?P<cid>\d+)/assignments$', controllers.assignmentAPI.AssignmentController.as_view()),
    re_path(r'^api/classes/(?P<cid>\d+)/assignments-file$', controllers.assignmentAPI.AssignmentFileController.as_view()),

    # Course-Class
    re_path(r'^api/course-classes-both$', controllers.courseAPI.CourseClassController.as_view()),

    # Get grade student
    re_path(r'^api/students/(?P<sid>\d+)/grades$', controllers.studentAPI.StudentGradeController.as_view()),

    # Get class's timetable
    re_path(r'^api/students/(?P<sid>\d+)/schedule$', controllers.classAPI.TimetableController.as_view()),

    # Send messages (deprecated)
    # re_path(r'^api/messages$', controllers.miscAPI.MessageController.as_view()),
    # re_path(r'^api/messages/usr1/(?P<user1_id>\d+)/usr2/(?P<user2_id>\d+)$', controllers.miscAPI.MessageController.as_view()),

    # Get attendance and tick true false
    re_path(r'^api/classes/(?P<cid>\d+)/attendance$', controllers.enrollmentAPI.AttendanceController.as_view()),
    re_path(r'^api/classes/(?P<cid>\d+)/students/(?P<sid>\d+)/attendance$', controllers.enrollmentAPI.AttendanceController.as_view()),

    # Send attendance report to parent email
    re_path(r'^api/classes/(?P<cid>\d+)/send-attendance$', controllers.enrollmentAPI.SendAttendanceController.as_view()),

    # Get and calculate class's statistics (Max Min Avg)
    re_path(r'^api/classes/(?P<cid>\d+)/statistics$', controllers.enrollmentAPI.ClassStatsController.as_view()),

    # Lấy thông tin chi tiết của lớp
    re_path(r'^api/classes/(?P<cid>\d+)/details$', controllers.miscAPI.DetailsController.as_view()),

    # Work ((Student) get, submit(post) and (Teacher) grading and delete )
    re_path(r'^api/classes/(?P<cid>\d+)/student/(?P<sid>\d+)/work/(?P<aid>\d+)$', controllers.workAPI.WorkController.as_view()),
    re_path(r'^api/classes/(?P<cid>\d+)/student/(?P<sid>\d+)/assignment/(?P<aid>\d+)$', controllers.workAPI.WorkController.as_view()),

    # Get and post reports
    re_path(r'^api/reports$', controllers.miscAPI.ReportController.as_view()),

    # Get summary
    re_path(r'^api/dashboard/admin$', controllers.miscAPI.AdminSummaryController.as_view()),
    re_path(r'^api/dashboard/teacher/(?P<tid>\d+)$', controllers.teacherAPI.TeacherSummaryController.as_view()),
    re_path(r'^api/dashboard/student/(?P<sid>\d+)$', controllers.studentAPI.StudentSummaryController.as_view())

    # re_path(r'^api/users', views.addUserAdmin),
    # re_path(r'^api/addAdmin', views.addAdmin)
]