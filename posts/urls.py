from django.contrib import admin
from django.urls import path, include
from . import views

name_app = "posts"

urlpatterns = [
    path('updatePost/', views.update_post, name='updatePost')
]
