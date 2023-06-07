from django.shortcuts import render,HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Thread,ChatMessage
from user.utils import user_data


# Create your views here.
@login_required
def home(request):
    threads = Thread.objects.by_user(user=request.user).prefetch_related('chatmessage_thread').order_by('-timestamp')
    context = {
        'Threads':threads,

    }

    return render(request,'home.html',context)