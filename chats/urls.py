from django.urls import path
from . import views

name_app = "chats"

urlpatterns = [
    path('u/',views.home,name='home'),
]