# -*- coding: utf-8 -*-

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, reverse
import random, re
from . import sendmail
from .models import user_acount, foods

def index(req):
    if req.method == "GET":
        return render(req, "index.html")


def food(req):
    if req.method == "GET":
        try:
            nickname = req.session.get("nickname")
        except:
            nickname = None
        print(nickname)
        if nickname:
            # 登录状态，可以点开购物车
            context = {"nickname": nickname}
            return render(req, "food.html", context)
        else:
            # 未登录，只能看到商品展示列表
            return render(req, "food.html")

def get_food(req):
    # 获取食物接口
    result = {"err": 1, "desc": "获取数据失败！", "foods": []}
    if req.method == "GET":
        try:
            all_food = foods.objects.all()
            result["err"] = 0
            result["desc"] = "获取数据成功！"
            for f in all_food:
                fid = f.fid
                fname = f.fname
                price = f.price
                size = f.size
                number = f.number
                ftype = f.ftype
                img_path = f.img_path
                f_info = {"fid": fid, "fname": fname, "price": price, "size": size, "number": number, "ftype": ftype, "img_path": img_path}
                result["foods"].append(f_info)
        except:
            print("仓库中没有商品!")
        return JsonResponse(result)
        


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
        try:
            uname = user_acount.objects.get(uname=username)
        except: 
            uname = None
        print(uname)
        if (not uname) or uname.upass != password:
            context = {"desc": "用户名或密码错误"}
            return render(req, "login.html", context)
        # 登录校验通过，将用户信息保存起来
        # 获取用户名
        nickname = uname.nickname
        print(nickname)
        req.session["nickname"] = nickname
        return redirect(reverse("food"))

def logout(req):
    if req.method == "GET":
        print("111")
        req.session.clear()
        print("222")
        return redirect("/login")

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
        if not (username and username.strip() and password and password2 and code and password == password2):
            return HttpResponse("信息不完整！")
        if not re.fullmatch(r"^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$", username):
            return HttpResponse("邮箱格式有误！")
        try:
            user = user_acount.objects.get(uname=username)
        except:
            user = None
        if user:
            return HttpResponse("邮箱已经被注册！")

        # 校验验证码，正确则注册成功！
        if code == verify_code:
            while True:
                # 随机生成用户名
                nickname = "ttf_" + str(random.randint(100000, 999999))
                # 检验该用户名是否存在
                try:
                    nick = user_acount.objects.get(nickname=nickname)
                except:
                    nick = None
                if not nick:
                    break
            user_acount.objects.create(uname=username, upass=password, nickname=nickname)
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

def user_center(req):
    if req.method == "GET":
        try:
            nickname = req.session.get("nickname")
        except:
            nickname = None
        print(nickname)
        if nickname:
            # 已经登录跳转个人中心
            context = {"nickname": nickname}
            return render(req, "user_center.html", context)
        else:
            # 没有登录跳转登录
            return redirect(reverse("index"))

def is_login(req):
    result = {"err": 1, "desc": "未登录！"}
    if req.method == "GET":
        try:
            nickname = req.session.get("nickname")
        except:
            nickname = None
        print(nickname)
        if nickname:
            result["err"] = 0
            result["desc"] = "已登录！"
        return JsonResponse(result)

def order(req):
    if req.method == "GET":
        return render(req,"success.html")
    elif req.method == "POST":
        order_name = req.POST.get("order_name")
        order_count = req.POST.get("order_count")
        order_price = req.POST.get("order_price")
        order_name = order_name.strip('[]').replace('"','').split(',')
        order_count = order_count.strip('[]').replace('"','').replace('×','').split(',')
        order_price = order_price.strip('[]').replace('"','').replace('￥','').split(',')
        print(order_name,order_count,order_price)
        return HttpResponse(req, "chenggong")
