from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib import auth
import django.contrib.auth.hashers as djh
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from .models import Listing,listing_form

def homepg(request):
    return render(request, "bookswap/index")

def login_view(request):
    if request.user.is_authenticated:
        return render(request, 'bookswap/homepg.html')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('Home'))
        else:
            form = AuthenticationForm(request.POST)
            return render(request, 'bookswap/login.html', {'form': form})
    else:
        form = AuthenticationForm()
        return render(request, 'bookswap/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))


def register(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('Home'))
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return HttpResponseRedirect(reverse('Home'))
        else:
            return render(request, 'bookswap/register.html', {'form': form})
    else:
        form = UserCreationForm()
        return render(request, 'bookswap/register.html', {'form': form})


def test(request):
    if request.method == 'POST':
       form = listing_form(request.POST,request.FILES)
       form.save()
       return render(request,"bookswap/create_listing.html",{'form':form})
    else:
        form=listing_form()
        return render(request,"bookswap/create_listing.html",{'form':form})