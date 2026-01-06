from rest_framework import serializers
from MainApp import models as m

class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = m.Admin
        fields = '__all__'

class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = m.Attendance
        fields = (
            'class_field',
            'student',
            'is_present'
        )

class AssignmentWithIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = m.Assignment
        fields = '__all__'

class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = m.Assignment
        fields = (
            'text_content',
            'file',
            'deadline',
            'class_field',
            'is_exam'
        )

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = m.Teacher
        fields = (
            'teacher_name',
            'teacher_gender',
            'teacher_email',
            'teacher_profession'
        )

class ClassWithCourseSerializer(serializers.ModelSerializer):
    class_teacher = serializers.PrimaryKeyRelatedField(queryset=m.Teacher.objects.all()) # Nested serialization

    class Meta:
        model = m.Class
        fields = (
            'class_name',
            'class_teacher',
            'class_semester',
            'course'
        )

class ClassWithIDSerializer(serializers.ModelSerializer):
    class_teacher = serializers.PrimaryKeyRelatedField(queryset=m.Teacher.objects.all())

    class Meta:
        model = m.Class
        fields = (
            'class_id',
            'class_name',
            'class_teacher',
            'class_semester'
        )

class TeacherWithIDSerializer(serializers.ModelSerializer):
    classes = ClassWithIDSerializer(source='class_set', many=True)
    class Meta:
        model = m.Teacher
        fields = (
            'teacher_id',
            'teacher_name',
            'teacher_gender',
            'teacher_email',
            'teacher_profession',
            'classes'
        )

class ClassSerializer(serializers.ModelSerializer):
    class_teacher = serializers.PrimaryKeyRelatedField(queryset=m.Teacher.objects.all()) # Nested serialization

    class Meta:
        model = m.Class
        fields = (
            'class_name',
            'class_teacher',
            'class_semester'
        )

class ClassTimetableSerializer(serializers.ModelSerializer):
    class Meta:
        model = m.ClassTimetable
        fields = (
            'day_of_week',
            'start_time',
            'end_time'
        )

class ClassWithTimetableSerializer(serializers.ModelSerializer):
    timetables = ClassTimetableSerializer(many=True, read_only=True)

    class Meta:
        model = m.Class
        fields = ('class_id', 'class_name', 'class_teacher', 'class_semester', 'timetables')

class CourseWithIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = m.Course
        fields = '__all__'

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = m.Course
        fields = (
            'course_name', 
            'course_semester',
            'course_midterm_coeff',
            'course_final_coeff',
            'course_credit'
        )

class StudentWithIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = m.Student
        fields = '__all__'

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = m.Student
        fields = (
            'student_name',
            'student_dob',
            'student_gender',
            'student_email',
            'parent_email',
            'student_phone_number',
            'student_specialization',
            'student_is_active'
        )


class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = m.Enrollment
        fields = (
            'class_field',
            'student',
            'withdrawal_date',
            'grade',
            'midterm',
            'final'
        )

class EnrollmentGradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = m.Enrollment
        fields = (
            'student',
            'midterm',
            'final',
            'grade'
        )

class EnrollmentGradeSubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = m.Enrollment
        fields = (
            'student',
            'class_field',
            'midterm',
            'final',
            'grade'
        )

class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = m.Report
        fields = (
            'type_of_bug',
            'description',
            'sender',
            'status'
        )

class SemesterWithIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = m.Semester
        fields = '__all__'

class SemesterSerializer(serializers.ModelSerializer):
    class Meta:
        model = m.Semester
        fields = (
            'name',
            'startDate',
            'endDate',
            'isActive'
        )

class WorkSerializer(serializers.ModelSerializer):
    class Meta:
        model = m.Work
        fields = (
            'assignment',
            'student',
            'class_field',
            'text_content',
            'file',
            'score'
        )

class WorkScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = m.Work
        fields = (
            'text_content',
            'file',
            'score'
        )

class UserloginSerializer(serializers.ModelSerializer):
    class Meta:
        model = m.Userlogin
        fields=(
            'username',
            'password',
            'useremail',
            'usertype',
            'relatedid'
        )