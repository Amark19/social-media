from django.shortcuts import render,HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Thread
from user.models import userData

# Create your views here.
@login_required(login_url='login')
def home(request):
    threads = Thread.objects.by_user(user=request.user).prefetch_related('chatmessage_thread').order_by('-timestamp')
    context = {
        'Threads':threads,
        'profile_pic':userData.objects.get(user_name=request.user.username).user_pic
    }

    return render(request,'home.html',context)