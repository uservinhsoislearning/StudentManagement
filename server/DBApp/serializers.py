from rest_framework import serializers
from .models import Admin, Parent, Student, Studentparent, Teacher, Course, Report, Semester, Assignment, Assignmentscore, Class, Enrollment, Work, ClassTimetable, Message
from Login.serializers import UserloginSerializer

class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = '__all__'

class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = (
            'text_content',
            'file',
            'deadline',
            'class_field',
            'is_exam'
        )

class AssignmentscoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignmentscore
        fields = (
            'assignment', 
            'student', 
            'score'
        )

class TeacherWithIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = (
            'teacher_id',
            'teacher_name',
            'teacher_gender',
            'teacher_email',
            'teacher_profession'
        )

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = (
            'teacher_name',
            'teacher_gender',
            'teacher_email',
            'teacher_profession'
        )

class ClassWithCourseSerializer(serializers.ModelSerializer):
    class_teacher = serializers.PrimaryKeyRelatedField(queryset=Teacher.objects.all()) # Nested serialization

    class Meta:
        model = Class
        fields = (
            'class_name',
            'class_teacher',
            'class_semester',
            'course',
            'start_time',
            'end_time'
        )

class ClassWithIDSerializer(serializers.ModelSerializer):
    class_teacher = serializers.PrimaryKeyRelatedField(queryset=Teacher.objects.all())

    class Meta:
        model = Class
        fields = (
            'class_id',
            'class_name',
            'class_teacher',
            'class_semester',
            'start_time',
            'end_time'
        )

class ClassSerializer(serializers.ModelSerializer):
    class_teacher = serializers.PrimaryKeyRelatedField(queryset=Teacher.objects.all()) # Nested serialization

    class Meta:
        model = Class
        fields = (
            'class_name',
            'class_teacher',
            'class_semester',
            'start_time',
            'end_time'
        )

class ClassTimetableSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassTimetable
        fields = (
            'day_of_week',
            'start_time',
            'end_time'
        )

class ClassWithTimetableSerializer(serializers.ModelSerializer):
    timetables = ClassTimetableSerializer(many=True, read_only=True)

    class Meta:
        model = Class
        fields = ('class_id', 'class_name', 'timetables')

class CourseWithIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = (
            'course_id',
            'course_name', 
            'course_semester',
            'course_midterm_coeff',
            'course_final_coeff'
        )

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = (
            'course_name', 
            'course_semester',
            'course_midterm_coeff',
            'course_final_coeff'
        )

class StudentWithIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = (
            'student_name',
            'student_dob',
            'student_gender',
            'student_email',
            'student_graduating_class',
            'student_phone_number',
            'student_specialization',
            'student_is_active',
            'student_school'
        )


class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
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
        model = Enrollment
        fields = (
            'student',
            'midterm',
            'final',
            'grade'
        )

class EnrollmentGradeSubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = (
            'student',
            'class_field',
            'midterm',
            'final',
            'grade'
        )


class MessageSerializer(serializers.ModelSerializer):
    sender = UserloginSerializer(read_only=True)
    receiver = UserloginSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'receiver', 'content', 'timestamp', 'is_read']

class ParentWithIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parent
        fields = '__all__'

class ParentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parent
        fields = (
            'parent_name',
            'parent_gender',
            'parent_email',
            'parent_phone_number',
            'parent_occupation'
        )

class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = (
            'type_of_bug',
            'description',
            'sender',
            'status'
        )

class SemesterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Semester
        fields = (
            'name',
            'startDate',
            'endDate',
            'isActive'
        )

class StudentparentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Studentparent
        fields = (
            'student',
            'relationship_to_student',
            'parent'
        )

class WorkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Work
        fields = (
            'assignment',
            'student',
            'text_content',
            'file',
            'score'
        )