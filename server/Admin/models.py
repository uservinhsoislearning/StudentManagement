from django.db import models

# Create your models here.
class Student(models.Model):
    student_name = models.CharField(max_length=255)
    student_dob = models.DateTimeField()
    student_gender = models.CharField(max_length=50)
    student_email = models.EmailField(max_length=255, unique=True)
    student_graduating_class = models.IntegerField()
    student_phone_number = models.CharField(max_length=20)
    student_specialization = models.CharField(max_length=255)
    student_is_active = models.BooleanField(default=True)
    student_school = models.CharField(max_length=50)