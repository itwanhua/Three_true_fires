from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('index', views.index),
    path('food', views.food),
    path('activity', views.activity),
    path('join', views.join),
    path('news', views.news),
    path('news_page', views.news_page),
    path('profile', views.profile),
    path('about', views.about),
    path('login', views.login),
    path('register', views.register),
    path('check_username', views.check_username),
    path('send_code', views.send_code),
]
