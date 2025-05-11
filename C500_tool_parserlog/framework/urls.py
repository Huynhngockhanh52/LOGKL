from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('index2', views.index2),
]