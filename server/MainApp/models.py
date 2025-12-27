from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator, MinValueValidator, MaxValueValidator
from django.contrib.auth.hashers import make_password

from django.utils import timezone
import os

class Admin(models.Model):
    admin_id = models.AutoField(primary_key=True)
    admin_username = models.CharField(unique=True, max_length=255)
    admin_password = models.CharField(max_length=255)
    admin_email = models.CharField(unique=True, max_length=255, blank=True, null=True)
    admin_name = models.CharField(max_length=255, blank=True, null=True)
    admin_is_active = models.BooleanField(blank=True, null=True)

    class Meta:
        db_table = 'admin'

def assignment_upload_path(instance, filename):
    return os.path.join('assignments', f"class_{instance.class_field.class_id}", filename)
class Assignment(models.Model):
    assignment_id = models.AutoField(primary_key=True)
    class_field = models.ForeignKey('Class', on_delete=models.CASCADE, db_column='class_id')
    text_content = models.TextField(
        max_length=10000,  # 1000 words roughly ~10,000 characters
        blank=True,
        null=True
    )
    file = models.FileField(
        upload_to=assignment_upload_path,
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'docx'])]
    )
    day_uploaded = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField()
    is_exam = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'assignment'

class Attendance(models.Model):
    session_id = models.AutoField(primary_key=True)
    class_field = models.ForeignKey('Class', on_delete=models.CASCADE, db_column='class_id')
    student = models.IntegerField()
    is_present = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'attendance'

class Class(models.Model):
    class_id = models.AutoField(primary_key=True)
    class_name = models.CharField(max_length=255)
    class_teacher = models.ForeignKey(
        'Teacher', 
        models.DO_NOTHING
    )
    class_semester = models.IntegerField(blank=True, null=True)
    course = models.ForeignKey(
        'Course',
        on_delete=models.CASCADE,
        related_name='classes'
    )

    class Meta:
        db_table = 'class'

class ClassTimetable(models.Model):
    DAY_CHOICES = [
        ('MON', 'Monday'),
        ('TUE', 'Tuesday'),
        ('WED', 'Wednesday'),
        ('THU', 'Thursday'),
        ('FRI', 'Friday'),
        ('SAT', 'Saturday'),
        ('SUN', 'Sunday'),
    ]

    timetable_id = models.AutoField(primary_key=True)
    class_field = models.ForeignKey(
        'Class',
        on_delete=models.CASCADE,
        related_name='timetables'
    )
    day_of_week = models.CharField(max_length=3, choices=DAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()
    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        db_table = 'class_timetable'


class Course(models.Model):
    course_id = models.AutoField(primary_key=True)
    course_name = models.CharField(max_length=255)
    course_semester = models.IntegerField(blank=True, null=True)
    course_midterm_coeff = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
        default=0.4
    )
    course_final_coeff = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
        default=0.6
    )
    course_credit = models.IntegerField(default=3)
    class Meta:
        db_table = 'course'

class Enrollment(models.Model):
    enrollment_id = models.AutoField(primary_key=True)
    student = models.ForeignKey(
        'Student', 
        models.DO_NOTHING
    )
    class_field = models.ForeignKey(
        Class, 
        models.DO_NOTHING, 
        db_column='class_id'
    )  # Field renamed because it was a Python reserved word.
    enrollment_date = models.DateTimeField(auto_now_add=True, null=True)
    withdrawal_date = models.DateTimeField(blank=True, null=True)
    grade = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(10.0)],
        blank=True,
        null=True
    )
    midterm = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(10.0)],
        blank=True,
        null=True
    )
    final = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(10.0)],
        blank=True,
        null=True
    )
    class Meta:
        db_table = 'enrollment'

class Message(models.Model):
    message_id = models.AutoField(primary_key=True)

    sender = models.ForeignKey(
        'Userlogin',
        on_delete=models.CASCADE,
        related_name='sent_messages'
    )
    receiver = models.ForeignKey(
        'Userlogin',
        on_delete=models.CASCADE,
        related_name='received_messages'
    )

    content = models.TextField(max_length=5000)
    timestamp = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)  # Track if the receiver has read the message

    class Meta:
        db_table = 'message'
        ordering = ['-timestamp']

class Parent(models.Model):
    parent_id = models.AutoField(primary_key=True)
    parent_name = models.CharField(max_length=255)
    parent_gender = models.CharField(max_length=50, blank=True, null=True)
    parent_email = models.CharField(unique=True, max_length=255, blank=True, null=True)
    parent_phone_number = models.CharField(max_length=20, blank=True, null=True)
    parent_occupation = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'parent'

class Registration(models.Model):
    connect_id = models.AutoField(primary_key=True)
    student = models.ForeignKey('Student', on_delete=models.CASCADE, db_column='student_id')
    class_field = models.ForeignKey('Class', on_delete=models.CASCADE, db_column='class_id')

    class Meta:
        db_table = 'registration'
        unique_together = ('student', 'class_field') 

class Report(models.Model):
    report_id = models.AutoField(primary_key=True)

    type_of_bug = models.TextField(
        max_length=1000,
        blank=True,
        null=True
    )

    description = models.TextField(
        max_length=10000,
        blank=True,
        null=True
    )

    sender = models.ForeignKey(
        'Userlogin',
        on_delete=models.SET_NULL,
        db_column='sender_id',
        null=True,
        blank=True,
        related_name='reports'
    )

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Resolved', 'Resolved'),
        ('Rejected', 'Rejected'),
    ]
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    class Meta:
        db_table = 'report'

class Semester(models.Model):
    semester_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    startDate = models.DateField()
    endDate = models.DateField()
    isActive = models.BooleanField(default=True)

    class Meta:
        db_table = 'semester'

class Student(models.Model):
    student_id = models.AutoField(primary_key=True)
    student_name = models.CharField(max_length=255, blank=True, null=True)
    student_dob = models.DateTimeField(blank=True, null=True)
    student_gender = models.CharField(max_length=50, blank=True, null=True)
    student_email = models.CharField(unique=True, max_length=255, blank=True, null=True)
    student_graduating_class = models.IntegerField(blank=True, null=True)
    student_phone_number = models.CharField(max_length=20, blank=True, null=True)
    student_specialization = models.CharField(max_length=255, blank=True, null=True)
    student_is_active = models.BooleanField(blank=True, null=True)
    student_school = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'student'


class Studentparent(models.Model):
    connect_id = models.AutoField(primary_key=True)
    student = models.ForeignKey(
        'Student',
        on_delete=models.CASCADE,
        db_column='student_id'
    )
    parent = models.ForeignKey(
        'Parent',
        on_delete=models.CASCADE,
        db_column='parent_id'
    )
    relationship_to_student = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'studentparent'
        unique_together = (('student', 'parent'),)

class Teacher(models.Model):
    teacher_id = models.AutoField(primary_key=True)
    teacher_name = models.CharField(max_length=255)
    teacher_gender = models.CharField(max_length=50, blank=True, null=True)
    teacher_email = models.CharField(unique=True, max_length=255, blank=True, null=True)
    teacher_profession = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'teacher'

class CourseTeacher(models.Model):
    connect_id = models.AutoField(primary_key=True)

    course = models.ForeignKey(
        'Course',
        on_delete=models.CASCADE,
        db_column='course_id'
    )

    teacher = models.ForeignKey(
        'Teacher',
        on_delete=models.CASCADE,
        db_column='teacher_id'
    )

    class Meta:
        db_table = 'course_teacher'
        unique_together = ('course', 'teacher')

def work_upload_path(instance, filename):
    return os.path.join('works', f"assignment_{instance.assignment.assignment_id}", f"student_{instance.student.student_id}", filename)

class Userlogin(models.Model):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(unique=True, max_length=255)
    password = models.CharField(max_length=255)
    useremail = models.CharField(unique=True, max_length=255)
    usertype = models.CharField(max_length=50)
    relatedid = models.IntegerField(blank=True, null=True)

    def save(self, *args, **kwargs):
        # Hash mat khau
        if not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'userlogin'

class Work(models.Model):
    work_id = models.AutoField(primary_key=True)
    assignment = models.ForeignKey('Assignment', on_delete=models.CASCADE, db_column='assignment_id')
    student = models.ForeignKey('Student', on_delete=models.CASCADE, db_column='student_id')
    class_field = models.ForeignKey('Class', on_delete=models.CASCADE, db_column='class_id')

    text_content = models.TextField(
        max_length=10000,
        blank=True,
        null=True
    )

    file = models.FileField(
        upload_to=work_upload_path,
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'docx'])]
    )

    day_uploaded = models.DateTimeField(auto_now_add=True)

    score = models.FloatField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0.0), MaxValueValidator(10.0)]
    )

    class Meta:
        db_table = 'work'