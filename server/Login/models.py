from django.db import models
from django.contrib.auth.hashers import make_password

# Create your models here.
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