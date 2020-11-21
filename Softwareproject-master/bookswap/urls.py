from django.urls import path
from django.urls import URLPattern
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("home",views.test,name="Home"),
] 