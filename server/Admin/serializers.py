from rest_framework import serializers
from DBApp.models import Student

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Student
        fields=('id',
                'student_name',
                'student_dob',
                'student_gender',
                'student_email',
                'student_graduating_class',
                'student_phone_number',
                'student_specialization',
                'student_is_active',
                'student_school')