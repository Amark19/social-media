
from django.shortcuts import render,HttpResponse,redirect
from django.urls import reverse
from django.contrib.auth.models import User
from .models import userData
from django.contrib.auth import authenticate, login,logout
import json
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
islogout=False
isregister=False
def get_user_data(r):
    global user_data
    user_data=userData.objects.values('name','user_desc','user_email','user_phone','user_birthday','user_pic').filter(user_name=r.user.username)
    # if userData.objects.values('user_pic').filter(user_name=r.user.username)
    return user_data
def login_user(request):
    global isregister
    login_valid=False
    if request.method == "POST":
        username=request.POST["username"]
        passw=request.POST["password"]
        user=authenticate(request,username=username,password=passw)
        if user is not None:
            login(request,user)
            return redirect('/')
        else:
            
            isregister=False
            login_valid=True
            return render(request,'login.html',{'isregister':isregister,'login_valid':login_valid})
    return render(request,'login.html',{'isregister':isregister,'login_valid':login_valid})

def register(request):
    global isregister
    if request.method == "POST":
        username=request.POST["username"]   
        request.session['username'] = username
        passw=request.POST["password"]
        user=User.objects.create_user(username,username,passw)
        user.save()
        name = request.POST['name']
        bio = request.POST['bio']
        email = request.POST['email']
        phoneno = request.POST['phonen']
        date = request.POST['bdate']
        pic=request.FILES.get('pic',False)
        pic.name=username+'.jpg'
        userData.objects.create(user_name=str(username),name=name,user_desc=bio,user_email=email,user_phone=str(phoneno),user_birthday=date,user_pic=pic)
        isregister=True
        return redirect('login/')
    
    else:
        isregister=False
        all_username = User.objects.all()
        all_username = [i.username for i in all_username]
        return render(request,'register.html',{'all_username':json.dumps(all_username)})

        
    return render(request,'register.html')

from django.views.decorators.cache import cache_control

@cache_control(no_cache=True, must_revalidate=True)
def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
        
        islogout=True
        messages.success(request,"Logged out successfully")
        return redirect("/login")

@cache_control(no_cache=True, must_revalidate=True)
def home(request):
    if not request.user.is_authenticated:

        return redirect('/login')
    elif request.user.is_authenticated:
        print(get_user_data(request))
        return render(request,'baseTemplate.html',{'profile_pic':get_user_data(request)[0]['user_pic']})

def profile(request,username):
    if not request.user.is_authenticated:
        return redirect('/login')
    elif username==request.user.username:
        return render(request,'profile.html',{'user_data':get_user_data(request),'profile_pic':get_user_data(request)[0]['user_pic']})
    else:
        return HttpResponse("404 not found")

@csrf_exempt
def edit_profile(request):
    if request.method == 'POST':
        if 'image' in request.FILES:
            from PIL import Image
            pic=request.FILES['image']
            Image.open(pic).save('media/'+ pic.name)
            userData.objects.filter(user_name=request.user.username).update(user_pic=pic)
        elif 'name' in request.POST:
            name = request.POST['name']
            bio = request.POST['bio']
            email = request.POST['email']
            phoneN = request.POST['phoneN']
            userData.objects.filter(user_name=request.user.username).update(name=name,user_desc=bio,user_email=email,user_phone=phoneN)
            # userData.objects.filter(user_name=request.user.username).update(user_pic=False)
        return render(request,'editProfile.html',{'user_data':get_user_data(request),'profile_pic':get_user_data(request)[0]['user_pic'],'isupdate':True})
    return render(request,'editProfile.html',{'user_data':get_user_data(request),'profile_pic':get_user_data(request)[0]['user_pic'],'isupdate':False})

def changePassword(request):
    if request.method == "POST":
        old_pass = request.POST['old_pass']
        new_pass = request.POST['new_pass']
        user = authenticate(request,username=request.user.username,password=old_pass)
        if user is not None:
            user.set_password(new_pass)
            user.save()
            return redirect('/login')
        else:
            
            return render(request,'changepassword.html',{'profile_pic':get_user_data(request)[0]['user_pic'],'ispassValid':True})
   

    return render(request,'changepassword.html',{'profile_pic':get_user_data(request)[0]['user_pic'],'ispassValid':False})