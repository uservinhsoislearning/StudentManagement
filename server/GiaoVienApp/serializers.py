from rest_framework import serializers
from .models import AttendanceRecord, AttendanceSession
from DBApp.serializers import StudentSerializer

class AttendanceSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttendanceSession
        fields = '__all__'

class AttendanceRecordSerializer(serializers.ModelSerializer):
    student = StudentSerializer(read_only=True)  # Nested student info (optional)

    class Meta:
        model = AttendanceRecord
        fields = (
            'student',
            'is_present'
        )