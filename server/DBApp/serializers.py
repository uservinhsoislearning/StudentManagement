from rest_framework import serializers
from .models import Admin, Class, Classstudent, Enrollment, Parent, Student, Studentparent, Teacher


class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = '__all__'


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


class ClassstudentSerializer(serializers.ModelSerializer):
    class_field = ClassSerializer(read_only=True)
    student = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Classstudent
        fields = '__all__'


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'


class EnrollmentSerializer(serializers.ModelSerializer):
    class_field = ClassSerializer(read_only=True)
    student = StudentSerializer(read_only=True)

    class Meta:
        model = Enrollment
        fields = '__all__'


class ParentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parent
        fields = '__all__'


class StudentparentSerializer(serializers.ModelSerializer):
    student = StudentSerializer(read_only=True)
    parent = ParentSerializer(read_only=True)

    class Meta:
        model = Studentparent
        fields = '__all__'
