from rest_framework import serializers
from .models import Admin, Class, Enrollment, Parent, Student, Studentparent, Teacher, Assignment, Course, Assignmentscore, Work, Report, Semester

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
            'class_field'
        )

class AssignmentscoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignmentscore
        fields = (
            'assignment', 
            'student', 
            'score'
        )

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ('teacher_name',
                  'teacher_gender',
                  'teacher_email',
                  'teacher_classes',
                  'teacher_profession')


class ClassSerializer(serializers.ModelSerializer):
    class_teacher = serializers.PrimaryKeyRelatedField(queryset=Teacher.objects.all()) # Nested serialization

    class Meta:
        model = Class
        fields = ('class_name',
                'class_teacher',
                'class_semester')

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = (
            'course_name', 
            'course_semester',
            'course_midterm_coeff',
            'course_final_coeff'
        )

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'


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

class ParentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parent
        fields = '__all__'

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
    student = StudentSerializer(read_only=True)
    parent = ParentSerializer(read_only=True)

    class Meta:
        model = Studentparent
        fields = '__all__'

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