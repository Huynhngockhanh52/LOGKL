from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('log/index', views.export_log_config),
    path('datasets/index', views.index_dataset),
    path('datasets/edit/<int:dataset_id>/', views.edit_dataset, name='edit_dataset'),
    path('datasets/detail/<int:dataset_id>/', views.detail_dataset, name='detail_dataset'),
]