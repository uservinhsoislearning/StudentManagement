# Generated by Django 5.1.7 on 2025-05-19 16:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DBApp', '0006_assignment_is_exam'),
        ('GiaoVienApp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attendancesession',
            name='class_field',
        ),
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('session_id', models.AutoField(primary_key=True, serialize=False)),
                ('student', models.IntegerField()),
                ('is_present', models.BooleanField(default=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('class_field', models.ForeignKey(db_column='class_id', on_delete=django.db.models.deletion.CASCADE, to='DBApp.class')),
            ],
            options={
                'db_table': 'attendance',
            },
        ),
        migrations.DeleteModel(
            name='AttendanceRecord',
        ),
        migrations.DeleteModel(
            name='AttendanceSession',
        ),
    ]
