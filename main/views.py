# -*- coding: utf-8 -*-

from django.http import HttpResponse, JsonResponse, HttpResponseServerError
from django.shortcuts import render, redirect, reverse
import random, re, time,threading
from . import sendmail
from .models import user_acount, foods, user_acount, user_info, orders, order_items

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
        req.session["nickname"] = nickname
        return redirect(reverse("food"))

def logout(req):
    if req.method == "GET":
        req.session.clear()
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
            return HttpResponseServerError
        if not re.fullmatch(r"^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$", username):
            return HttpResponseServerError
        try:
            user = user_acount.objects.get(uname=username)
        except:
            user = None
        if user:
            return HttpResponseServerError

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
            # # 由于外键约束，nickname=对象 才能创建成功
            # nick = user_acount.objects.get(nickname=nickname)
            # user_info.objects.create(nickname=nick)
            user_info.objects.create(nickname=nickname)
            return redirect("/login")
        else:
            print("验证码错误！")
            context = {"desc": "邮箱验证码错误！"}
            return render(req, "register.html", context)

def check_username(req):
    if req.method == "GET":
        username = req.GET.get("username")
        if not username:
            return HttpResponseServerError
        result = {"err": 1, "desc": "该邮箱已被注册！"}
        # 查找用户名是否存在
        try:
            user = user_acount.objects.get(uname=username)
        except:
            user = None
        if not user:
            result["err"] = 0
            result["desc"] = "该邮箱可以注册！"
        return JsonResponse(result)


def send_code(req):
    result = {"err": 1, "desc": "內部错误！"}
    if req.method == "POST":
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
            return redirect(reverse("login"))
    if req.method == "POST":
        # 用于用户修改个人信息
        # 防止恶意请求进入个人中心
        try:
            nickname = req.session.get("nickname")
        except:
            nickname = None
        if nickname:
            # 正常状态，收集表单信息入库
            new_nickname = req.POST.get("nickname")
            realname = req.POST.get("realname")
            phone = req.POST.get("phone")
            address = req.POST.get("address")
            remarks = req.POST.get("remarks")

            # 未修改用户名
            if nickname == new_nickname:
                user_info.objects.filter(nickname=nickname).update(realname=realname, phone=phone, target_addr=address, remarks=remarks)
                context = {"desc": "修改成功！", "nickname": nickname}

            # 修改了用户名
            # 校验修改后的用户名已经存在
            else:
                print(nickname, "session")
                try:
                    new_nickname_is_exist = user_acount.objects.get(nickname=new_nickname)
                except:
                    new_nickname_is_exist = None
                print(new_nickname_is_exist)
                if new_nickname_is_exist:
                    context = {"desc": "修改失败，该用户名已经被注册了", "nickname": nickname}
                else:
                    # 不存在则可以修改入库
                    print(nickname, new_nickname)

                    try: # 两表同时修改
                        user_acount.objects.filter(nickname=nickname).update(nickname=new_nickname)
                        user_info.objects.filter(nickname=nickname).update(nickname=new_nickname, realname=realname, phone=phone, target_addr=address, remarks=remarks)
                        # 用户名改变，session信息改变
                        req.session["nickname"] = new_nickname
                        context = {"desc": "修改成功！", "nickname": new_nickname}
                    except:
                        context = {"desc": "修改失败!", "nickname": nickname}
            return render(req, "user_center.html", context)
        else:
            # 没有携带Cookie的POST请求直接跳转主页
            return redirect(reverse("index"))

def is_login(req):
    result = {"err": 1, "desc": "未登录！"}
    if req.method == "GET":
        try:
            nickname = req.session.get("nickname")
        except:
            nickname = None
        if nickname:
            result["err"] = 0
            result["desc"] = "已登录！"
        return JsonResponse(result)

    

def get_user_info(req):
    result = {"err": 1, "user_info": {}}
    if req.method == "GET":
        # 获取用户名
        nickname = req.GET.get("nickname")
        print(nickname)
        user = user_info.objects.get(nickname=nickname)
        realname = user.realname
        phone = user.phone
        target_addr = user.target_addr
        remarks = user.remarks

        result["err"] = 0
        result["user_info"] = {"realname": realname, "phone": phone, "target_addr": target_addr, "remarks": remarks}
        return JsonResponse(result)



def order(req):
    if req.method == "GET":
        return render(req,"success.html")
    elif req.method == "POST":
        order_name = req.POST.get("order_name")   #获取购物车的单品菜名列表
        order_count = req.POST.get("order_count") #获取购物车的单品数量列表
        order_price = req.POST.get("order_price") #获取购物车的单品总价格列表
        sum_pic = req.POST.get("sum_price")       #获取购物车的总价格
        sum_cnt = req.POST.get("sum_count")       #获取购物车的总数量
        order_name = order_name.strip('[]').replace('"','').split(',')
        order_count = order_count.strip('[]').replace('"','').replace('×','').split(',')
        order_price = order_price.strip('[]').replace('"','').replace('￥','').split(',')
        sum_pic = sum_pic.replace('￥','')
        sum_cnt = sum_cnt.replace("件",'')
        data = zip(order_name,order_count,order_price)
        
        #收件信息
        nick_name = req.session.get("nickname")
        customer = user_info.objects.get(nickname=nick_name)
        cus_name = customer.realname
        cus_phone = customer.phone
        cus_addr = customer.target_addr
        remarks = customer.remarks

        #获取当前时间
        now = int(time.time())
        timeArray = time.localtime(now)
        ntime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        order_id = time.strftime("%Y%m%d%H%M%S", timeArray) + nick_name

        context = {"order_id":order_id,"order_list":data,'sum_cnt':sum_cnt,'sum_pic':sum_pic,"time":ntime,"customer":cus_name,
        "phone":cus_phone,"target_addr":cus_addr,"remarks":remarks}
        print(context)


        return render(req,"success.html",context)


def success(req):
    if req.method == "GET":
        return render(req,"order.html")
    elif req.method == "POST":
        err={}
        order_name = req.POST.get("order_name")  #订单单品菜名列表
        order_count = req.POST.get("order_count") #订单单品数量列表
        order_price = req.POST.get("order_price") #订单单品总价格列表
        order_id = req.POST.get("order_id")    #订单流水号
        time = req.POST.get("time")        #订单时间
        customer = req.POST.get("customer")    #收件人姓名
        phone = req.POST.get("phone")       #收件人电话
        target_addr = req.POST.get("target_addr") #收件地址
        sum_cnt = req.POST.get("sum_cnt")     #订单合计价格
        sum_pic = req.POST.get("sum_pic")     #订单合计数量
        remarks = req.POST.get('remarks')     #订单备注
        nickname = req.session.get("nickname")   #账号名

        order_name = order_name.strip('[]').replace('"','').split(',')
        order_count = order_count.strip('[]').replace('"','').split(',')
        order_price = order_price.strip('[]').replace('"','').split(',')
        
        # print(order_name,order_count,order_price)
        # print(order_id,time,customer,phone,sum_pic,target_addr,nickname)
        try:
            #存入订单表
            orders.objects.create(order_id=order_id,otime=time,customer=customer,
            phone=phone,total_money=sum_pic,target_addr=target_addr,nickname=nickname)
            
            #存入订单详情表
            oid = orders.objects.get(order_id=order_id)
            for n,num,pic in zip(order_name,order_count,order_price):
                order_items.objects.create(oname=n,onumber=num,oprice=pic,order_id=oid)

            user_info.objects.filter(nickname=nickname).update(remarks=remarks)
            
            err["code"] = 0 #订单入库成功

            s = ""
            for i in range(len(order_name)):
                s += order_name[i] + "  ×" + order_count[i] + "  " + order_price[i]+ " ￥" + "\n"

            msg = " \
订单号：{} \n\
订单时间：{} \n\
收货人：{} \n\
手机号：{} \n\
收获地址：{} \n\
订单备注：{} \n\
商品列表：\n\n \
{} \
".format(order_id, time, customer, phone, target_addr, remarks, s)

            print(msg)

            threading.Thread(target=sendmail.send_mail,args=(msg, "wh@ithz.xyz")).start()

        except Exception as e:
            print(e)
            err['code'] = 1 #订单入库失败
        # print('#########################')
        return JsonResponse(err)


def order_center(req):
    try:
        nickname = req.session["nickname"]
    except:
        nickname = None
    if not nickname:
        return redirect(reverse("login"))
 
    if req.method == "GET":
        return render(req, "order_center.html")

    if req.method == "POST":
        result = {'err':1, "info": []}
        nickname = req.session.get('nickname')
        print(nickname)
        try:
            order_info = orders.objects.filter(nickname=nickname)
            print(order_info)
            if order_info:
                for info in order_info:
                    order_id = info.order_id
                    otime = info.otime
                    customer = info.customer
                    phone = info.phone
                    total_money = info.total_money
                    target_addr = info.target_addr
                    result["info"].append({"order_id":order_id,"otime":otime,"customer":customer,"phone":phone,
                    "total_money":total_money,"target_addr":target_addr,"nickname":nickname})
                    print(result)
                result["err"] = 0
        except Exception as e:
            print(e)
        return JsonResponse(result)




def get_history_order_info(req):

    if req.method == 'POST':
        order_id = req.POST.get('order_id')  #获取订单号
        result = {"err": 1, "item": []}
        try:
            items = order_items.objects.filter(order_id=order_id)
            for item in items:
                oname = item.oname
                onumber = item.onumber
                oprice = item.oprice
                result["item"].append({"order_id":order_id,"oname":oname,"onumber":onumber,"oprice":oprice})
            result["err"] = 0
            print(result)
        except Exception as e:
            print(e)
        return JsonResponse(result)
