"""memeway URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect


def index(request):
    return render(request, "index.html")


def session(request):
    if request.user.is_authenticated:
        return redirect("rater:index")
    return render(request, "register.html")


def signup_controller(request):
    if request.method != "POST":
        redirect("session")
    pass


def login_controller(request):
    if request.method != "POST":
        return render(request, "login.html")
    pass


@login_required
def logout_controller(request):
    logout(request)
    return redirect("index")


urlpatterns = [
    url(r'^$', index, name="index"),
    url(r'^session$', session, name="session"),
    url(r'^session/signup$', signup_controller, name="signup"),
    url(r'^session/login$', login_controller, name="login"),
    url(r'^logout$', login_controller, name="logout"),
    url(r'^rater/', include('rater.urls', namespace="rater")),
    url(r'^admin/', admin.site.urls),
]
