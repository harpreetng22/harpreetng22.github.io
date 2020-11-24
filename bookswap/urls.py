from django.urls import path
from django.urls import URLPattern
from . import views


urlpatterns = [
    path("", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listing", views.manage_listing, name="listing"),
    path("vlisting",views.view_listing,name="view_listing"),
    path("match",views.matches,name="match"),
    path("request",views.request,name="request"),
]