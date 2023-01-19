from django.urls import path
from . import views

urlpatterns = [
    # path("", views.index, name="index"), #calls index by default in views.py
    path("", views.home, name="home"),
    path("<str:loc>", views.index, name="index"),
    path("create/", views.create, name="create"),


]
