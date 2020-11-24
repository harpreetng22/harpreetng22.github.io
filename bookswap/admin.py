from django.contrib import admin

# Register your models here.
from django.contrib.auth.models import User
from .models import Listing,Request

admin.site.register(Listing)
admin.site.register(Request)