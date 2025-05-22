from django.db import models

# Create your models here.

class Attendance(models.Model):
    session_id = models.AutoField(primary_key=True)
    class_field = models.ForeignKey('DBApp.Class', on_delete=models.CASCADE, db_column='class_id')
    student = models.IntegerField()
    is_present = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'attendance'