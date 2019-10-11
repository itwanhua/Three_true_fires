from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('index', views.index, name="index"),
    path('food', views.food, name="food"),
    path('activity', views.activity),
    path('join', views.join),
    path('news', views.news),
    path('news_page', views.news_page),
    path('profile', views.profile),
    path('about', views.about),
    path('login', views.login, name="login"),
    path('register', views.register),
    path('check_username', views.check_username),
    path('send_code', views.send_code),
    path('get_food', views.get_food),
    path('logout', views.logout),
    path('is_login', views.is_login),
    path('user_center', views.user_center),
    path('order',views.order),
    path('get_user_info',views.get_user_info),
    path('order_center', views.order_center),
    path('submit', views.success),
    path('get_history_order_info', views.get_history_order_info),
]
