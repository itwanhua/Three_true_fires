# -*- coding: utf-8 -*-

from django.db import models

# Create your models here.

class user_acount(models.Model):
    uname = models.CharField(max_length=100, primary_key=True)
    upass = models.CharField(max_length=100)
    nickname = models.CharField(max_length=100, unique=True)

class foods(models.Model):
    fid = models.AutoField(auto_created=1000, primary_key=True)
    fname = models.CharField(max_length=255, unique=True)
    price = models.CharField(max_length=50)
    size = models.CharField(max_length=11)
    number = models.IntegerField()
    ftype = models.CharField(max_length=30)
    img_path = models.CharField(max_length=50)

class orders(models.Model):
    order_id = models.CharField(max_length=100, primary_key=True) # 流水号，时间+顾客id
    otime = models.CharField(max_length=50) # 下单时间
    customer = models.CharField(max_length=100) # 顾客id或者姓名
    phone = models.CharField(max_length=11) # 电话
    total_money = models.CharField(max_length=50) # 总价
    target_addr = models.CharField(max_length=255) # 地址
    nickname = models.CharField(max_length=100) # 可重复

class order_items(models.Model):
    oi_id = models.AutoField(auto_created=10000, primary_key=True) 
    oname = models.CharField(max_length=100) # 菜名
    onumber = models.IntegerField() # 单个菜数量
    oprice = models.CharField(max_length=50) # 单个菜点的总价???
    order_id = models.ForeignKey(orders, to_field="order_id", on_delete=models.CASCADE) # 外键

class user_info(models.Model):
    nickname = models.CharField(max_length=100, unique=True) # 用户名（账号昵称）
    realname = models.CharField(max_length=100, unique=True, null=True) # 真名
    phone = models.CharField(max_length=11, null=True) # 默认电话
    target_addr = models.CharField(max_length=255, null=True) # 默认地址
    remarks = models.CharField(max_length=255, null=True) # 默认备注














