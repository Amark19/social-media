from django.urls import path
from . import views

name_app = "chats"

urlpatterns = [
    path('',views.home,name='home'),
]