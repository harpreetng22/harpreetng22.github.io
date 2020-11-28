from typing import List
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.db.models.query_utils import check_rel_lookup_compatibility
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib import auth
import django.contrib.auth.hashers as djh
from django.contrib.auth.forms import UserCreationForm, UserModel
from django.contrib.auth.forms import AuthenticationForm
from django.forms import modelformset_factory
from bookswap.models import Listing,listing_form,Request
from django.contrib.auth.decorators import login_required


@login_required(login_url='/')
def manage_listing(request):
    if request.method == 'POST':
        form = listing_form(request.POST, request.FILES)
        if form.is_valid():
            f=form.save(commit=False)
            f.user=request.user
            f.save()
        return render(request, "bookswap/manage_listing.html", {'formset': form})
    else:
        form = listing_form()
        return render(request, "bookswap/manage_listing.html", {'formset': form})


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
            return HttpResponseRedirect(reverse('view_listing'))
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
        return HttpResponseRedirect(reverse('view_listing'))
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return HttpResponseRedirect(reverse('view_listing'))
        else:
            return render(request, 'bookswap/register.html', {'form': form})
    else:
        form = UserCreationForm()
        return render(request, 'bookswap/register.html', {'form': form})


def request(request):
    for i in Listing.objects.all():
        print(request.session['uid'])
        print(i.id)
        if (i.id==request.session['uid']):
            print("here")
            obj=Request(listing_id=i,requested_by=request.user)
            print(obj.listing_id)
            obj.save()

    return render(request,"bookswap/homepg.html")

def view_listing(request):
     if request.user.is_authenticated:
       data=Listing.objects.filter(check_req=0)
       return render(request,"bookswap/view_listings.html",{
        'data':data
         })
     else:
         return render(request,"bookswap/homepg.html")

def matches(request):
  if request.method == 'GET':
    if request.user.is_authenticated:
     uname=request.user.username
     j=0
     data=Listing.objects.filter(check_req=0)
     data1=Listing.objects.filter(check_req=1)
     for i in Listing.objects.all():
      if(str(i.user)==uname):
        j=1
        request.session['uid'] =i.id
     if j==1:
      return render(request,"bookswap/matches.html",{
        'data':data,'requests':data1,
         })
     else:
         return render(request,"bookswap/nomatch.html")
    else:
         return render(request,"bookswap/homepg.html")
  if request.method == 'POST':
      if 'send_request' in request.POST:
        uname=request.user.username
        print(request.POST.get('listing'))
        data=Listing.objects.all()
        for i in Listing.objects.all():
            if(str(i.user)==uname):
                for j in Listing.objects.all():
                    if(str(j.first_name)==request.POST.get('listing') and (i.have)==(j.want) and (j.have)==(i.want)):
                        j.check_req=1
                        i.check_req=1
                        j.save()
                        i.save()
        
        return render(request,"bookswap/homepg.html")
      if 'accept_request' in request.POST:
        uname=request.user.username
        print(request.POST.get('acc_request'))
        data=Listing.objects.all()
        for i in Listing.objects.all():
            if(str(i.user)==uname):
                for j in Listing.objects.all():
                    if(str(j.first_name)==request.POST.get('acc_request') and (i.have)==(j.want) and (j.have)==(i.want)):
                        j.check_req=2
                        i.check_req=2
                        j.save()
                        i.save()
                    if(str(j.first_name)!=request.POST.get('acc_request') and (i.have)==(j.want) and (j.have)==(i.want)):
                        j.check_req=0
                        j.save()
                        
        return render(request,"bookswap/test.html")
      elif 'rej_request' in request.POST:
        print('reject')
        uname=request.user.username
        print(request.POST.get('acc_request'))
        data=Listing.objects.all()
        for i in Listing.objects.all():
            if(str(i.user)==uname):
                for j in Listing.objects.all():
                    if(str(j.first_name)==request.POST.get('acc_request') and (i.have)==(j.want) and (j.have)==(i.want)):
                        j.check_req=0
                        i.check_req=0
                        j.save()
                        i.save()
                    if(str(j.first_name)!=request.POST.get('acc_request') and (i.have)==(j.want) and (j.have)==(i.want)):
                        print('test')
                        j.check_req=0
                        i.check_req=0
                        j.save()
                        i.save()
        
        return render(request,"bookswap/test.html")

def active_listings(request):
     data=Listing.objects.filter(check_req=0)
     data1=Listing.objects.filter(check_req=1)
     if data==None and data1==None:
      return render(request,'bookswap/nomatch.html',{
         'data':data,'data1':data1
      })
     else:
         return render(request,'bookswap/active_listings.html',{
         'data':data,'data1':data1
      })
def test(request):
     pass
