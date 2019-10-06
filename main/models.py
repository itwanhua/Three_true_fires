from django.db import models

# Create your models here.

class user_acount(models.Model):
    uname = models.CharField(max_length=100, primary_key=True)
    upass = models.CharField(max_length=100)

