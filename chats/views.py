from django.shortcuts import render,HttpResponse
from .models import Thread,ChatMessage
from user.utils import user_data


# Create your views here.
def home(request):
    threads = Thread.objects.by_user(user=request.user).prefetch_related('chatmessage_thread').order_by('-timestamp')
    context = {
        'Threads':threads,

    }

    return render(request,'home.html',context)