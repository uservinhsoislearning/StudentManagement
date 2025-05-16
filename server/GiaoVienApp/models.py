from django.db import models

# Create your models here.
class AttendanceSession(models.Model):
    session_id = models.AutoField(primary_key=True)
    class_field = models.ForeignKey('DBApp.Class', on_delete=models.CASCADE, db_column='class_id')
    date = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'attendance_session'

class AttendanceRecord(models.Model):
    record_id = models.AutoField(primary_key=True)
    session = models.ForeignKey('AttendanceSession', on_delete=models.CASCADE, db_column='session_id')
    enrollment = models.ForeignKey('DBApp.Enrollment', on_delete=models.CASCADE, db_column='enrollment_id')
    student = models.ForeignKey('DBApp.Student', on_delete=models.CASCADE, db_column='student_id')
    is_present = models.BooleanField(default=False)

    class Meta:
        db_table = 'attendance_record'
        unique_together = ('session', 'student')  # One record per student per session