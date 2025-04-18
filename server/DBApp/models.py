from django.db import models

# Create your models here.
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Admin(models.Model):
    admin_id = models.AutoField(primary_key=True)
    admin_username = models.CharField(unique=True, max_length=255)
    admin_password = models.CharField(max_length=255)
    admin_email = models.CharField(unique=True, max_length=255, blank=True, null=True)
    admin_name = models.CharField(max_length=255, blank=True, null=True)
    admin_is_active = models.BooleanField(blank=True, null=True)

    class Meta:
        db_table = 'admin'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Class(models.Model):
    class_id = models.AutoField(primary_key=True)
    class_name = models.CharField(max_length=255)
    class_teacher = models.ForeignKey('Teacher', models.DO_NOTHING)
    class_semester = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'class'


class Classstudent(models.Model):
    class_field = models.OneToOneField(Class, models.DO_NOTHING, db_column='class_id', primary_key=True)  # Field renamed because it was a Python reserved word. The composite primary key (class_id, student_id) found, that is not supported. The first column is selected.
    student = models.ForeignKey('Student', models.DO_NOTHING)

    class Meta:
        db_table = 'classstudent'
        unique_together = (('class_field', 'student'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Enrollment(models.Model):
    enrollment_id = models.AutoField(primary_key=True)
    student = models.ForeignKey('Student', models.DO_NOTHING)
    class_field = models.ForeignKey(Class, models.DO_NOTHING, db_column='class_id')  # Field renamed because it was a Python reserved word.
    enrollment_date = models.DateField(blank=True, null=True)
    withdrawal_date = models.DateField(blank=True, null=True)
    grade = models.CharField(max_length=5, blank=True, null=True)

    class Meta:
        db_table = 'enrollment'


class Parent(models.Model):
    parent_id = models.AutoField(primary_key=True)
    parent_firstname = models.CharField(max_length=255)
    parent_lastname = models.CharField(max_length=255)
    parent_gender = models.CharField(max_length=50, blank=True, null=True)
    parent_email = models.CharField(unique=True, max_length=255, blank=True, null=True)
    parent_phone_number = models.CharField(max_length=20, blank=True, null=True)
    parent_address = models.CharField(max_length=255, blank=True, null=True)
    parent_occupation = models.CharField(max_length=255, blank=True, null=True)
    parent_relationship_to_student = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'parent'


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
    student = models.OneToOneField(Student, models.DO_NOTHING, primary_key=True)  # The composite primary key (student_id, parent_id) found, that is not supported. The first column is selected.
    parent = models.ForeignKey(Parent, models.DO_NOTHING)
    relationship_to_student = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'studentparent'
        unique_together = (('student', 'parent'),)


class Teacher(models.Model):
    teacher_id = models.AutoField(primary_key=True)
    teacher_name = models.CharField(max_length=255)
    teacher_gender = models.CharField(max_length=50, blank=True, null=True)
    teacher_email = models.CharField(unique=True, max_length=255, blank=True, null=True)
    teacher_classes = models.CharField(max_length=255, blank=True, null=True)
    teacher_profession = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'teacher'
