# -*- coding: utf-8 -*-

from django.db import models

# Create your models here.

class user_acount(models.Model):
    uname = models.CharField(max_length=100, primary_key=True)
    upass = models.CharField(max_length=100)

class foods(models.Model):
    fid = models.AutoField(auto_created=1000, primary_key=True)
    fname = models.CharField(max_length=255, unique=True)
    price = models.CharField(max_length=50)
    size = models.CharField(max_length=11)
    number = models.IntegerField()
    ftype = models.CharField(max_length=30)
    img_path = models.CharField(max_length=50)




