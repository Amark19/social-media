
from django.contrib import admin
from django.urls import path, include
from . import views
from posts import views as post_views

urlpatterns = [
    path('', views.home, name='home'),
    path('login', views.login_user, name='login'),
    path('register', views.register, name='register'),
    path('logout/', views.logout_user, name="Logout"),
    path('<str:username>/', views.profile, name='profile'),
    path('accounts/edit/', views.edit_profile, name='edit_profile'),
    path('accounts/changePassword/', views.changePassword, name='changePassword'),
    path('post/createPost/', post_views.create_post, name='createPost'),
    path('post/<int:post_id>/', post_views.view_post, name='viewPost'),
]