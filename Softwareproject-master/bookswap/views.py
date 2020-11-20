from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.models import User,auth


def homepg(request):
    return render(request, "bookswap/index")

def login_view(request):
    if request.method == "POST":

        

        password1 = request.POST.get("Password")
        username = request.POST.get("username")
        print(username)
        print(password1)
        user = auth.authenticate(username=username, password=password1)

        print(user)
        if user is not None:
            auth.login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "bookswap/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "bookswap/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        first_name=request.POST["first_name"]
        last_name = request.POST["last_name"]
        username = request.POST["username"]
        email = request.POST["email"]

        
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]
        if password1 != password2:
            return render(request, "bookswap/register.html", {
                "message": "Passwords must match."
            })

       
        try:
            user = User.objects.create_user(username=username, email=email, password=password1,first_name=first_name,last_name=last_name)
            user.save()
        except IntegrityError:
            return render(request, "bookswap/register.html", {
                "message": "Username already taken."
            })

        auth.login(request, user)
        return HttpResponseRedirect(reverse("Home"))
    else:
        return render(request, "bookswap/register.html")
