from django.db import models

# Create your models here.
class Userlogin(models.Model):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(unique=True, max_length=255)
    password = models.CharField(max_length=255)
    usertype = models.CharField(max_length=50)
    relatedid = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'userlogin'