# Generated by Django 5.1.7 on 2025-05-18 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Userlogin',
            fields=[
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=255, unique=True)),
                ('password', models.CharField(max_length=255)),
                ('useremail', models.CharField(max_length=255, unique=True)),
                ('usertype', models.CharField(max_length=50)),
                ('relatedid', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'userlogin',
            },
        ),
    ]
