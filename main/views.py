# -*- coding: utf-8 -*-

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
import random
from . import sendmail
from .models import user_acount

def index(req):
    if req.method == "GET":
        return render(req, "index.html")


def food(req):
    if req.method == "GET":
        return render(req, "food.html")


def activity(req):
    if req.method == "GET":
        return render(req, "activity.html")


def join(req):
    if req.method == "GET":
        return render(req, "join.html")


def news(req):
    if req.method == "GET":
        return render(req, "news.html")


def news_page(req):
    if req.method == "GET":
        return render(req, "news_page.html")


def profile(req):
    if req.method == "GET":
        return render(req, "profile.html")


def about(req):
    if req.method == "GET":
        return render(req, "about.html")


def login(req):
    if req.method == "GET":
        return render(req, "login.html")
    elif req.method == "POST":
        username = req.POST.get("username")
        password = req.POST.get("password")

        uname = user_acount.objects.get(uname=username)
        print(uname)
        if uname.upass != password:
            context = {"desc": "用户名或密码错误"}
            return render(req, "login.html", context)
        # 登录校验通过，将用户信息保存起来

        return redirect("/")

def register(req):
    if req.method == "GET":
        return render(req, "register.html")
    elif req.method == "POST":
        username = req.POST.get("username")
        password = req.POST.get("password")
        password2 = req.POST.get("password2")
        code = req.POST.get("code")
        try:
            verify_code = req.session.get(username)
        except:
            verify_code == None
        print(username, password, password2, code, verify_code)
        # 后端二次校验表单数据

        # 校验验证码，正确则注册成功！
        if code == verify_code:
            print("注册成功")
            user_acount.objects.create(uname=username, upass=password)
            return redirect("/login")
        else:
            print("验证码错误！")
            context = {"desc": "邮箱验证码错误！"}
            return render(req, "register.html", context)

def check_username(req):
    if req.method == "GET":
        username = req.GET.get("username")
        print(username)
        if not username:
            abort(500)
        result = {"err": 1, "desc": "该邮箱已被注册！"}
        # 查找用户名是否存在
        try:
            user = user_acount.objects.get(uname=username)
        except:
            user = None
        if not user:
            print("可以注册！")
            result["err"] = 0
            result["desc"] = "该邮箱可以注册！"
        return JsonResponse(result)


def send_code(req):
    print("1111")
    result = {"err": 1, "desc": "內部错误！"}
    if req.method == "POST":
        print("2222")
        email = req.POST.get("email")
        print(email)
        # 发送验证码
        verify_code = str(random.randint(100000, 999999))
        data = verify_code
        r = sendmail.send_mail(data, email)
        if r == 0:
            # 发送邮箱验证码成功
            req.session[email] = verify_code
            print(verify_code)
            result["err"] = 0
            result["desc"] = "发送邮箱验证码成功！"
        return JsonResponse(result)