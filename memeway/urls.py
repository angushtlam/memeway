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
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from rater.models import User, ChatRoom, Message


def index(request):
    return render(request, "index.html")


def session(request):
    if request.user.is_authenticated:
        return redirect("rater:index")
    return render(request, "register.html")


def register_controller(request):
    if request.method != "POST":
        redirect("session")

    username = request.POST.get("username", "").lower()
    password = request.POST.get("password", "")
    gender = request.POST.get("gender", "")

    if User.objects.filter(username=username).first():
        messages.error(request, "Someone already took that username! :o")
        return redirect("session")

    user = User.objects.create_user(username, password)
    user.gender = gender
    user.save()

    memecat = User.objects.filter(username="memecat").first()

    user.matches.add(memecat)
    user.liked.add(memecat)
    user.save()

    chat = ChatRoom.objects.create()
    chat.users.add(memecat)
    chat.users.add(user)
    chat.save()

    message = Message.objects.create(text="I am memecat, hear me RAWR. I am your savior and helper of all things memes! Ask any of your questions here!",
                                     sender=memecat, chat=chat)
    message.save()

    user = authenticate(username=username, password=password)
    login(request, user)

    return redirect("rater:welcome")


def login_controller(request):
    if request.user.is_authenticated:
        return redirect("rater:index")
    if request.method != "POST":
        return render(request, "login.html")
    username = request.POST.get("username", "")
    password = request.POST.get("password", "")
    user = authenticate(username=username, password=password)

    if user is not None:
        login(request, user)
        # Redirect to a success page.
        if user.memes.all() == 0:
            return redirect("rater:welcome")
        return redirect("rater:index")
    else:
        messages.error(request, "Invalid credentials! Try again.")
        return redirect("login")


@login_required
def logout_controller(request):
    logout(request)
    return redirect("index")


urlpatterns = [
    url(r'^$', index, name="index"),
    url(r'^session$', session, name="session"),
    url(r'^session/register$', register_controller, name="register"),
    url(r'^session/login$', login_controller, name="login"),
    url(r'^logout$', logout_controller, name="logout"),
    url(r'^discover/', include('rater.urls', namespace="rater")),
    url(r'^admin/', admin.site.urls),
]
