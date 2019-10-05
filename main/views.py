from django.http import HttpResponse
from django.shortcuts import render

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