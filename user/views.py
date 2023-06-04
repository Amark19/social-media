
from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.db.models import Q
from .models import userData, userFollowers
from posts.models import Post
from django.contrib.auth import authenticate, login, logout
import json
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from .utils import user_data
from posts.utils import post_util
from chats.models import Thread


# Create your views here.
islogout = False
isregister = False


def userObj(username):
    userObj = user_data.get_user_data(username)[0]
    userObj['is_following'], userObj['is_followed'] = False, False
    return userObj


def login_user(request):
    global isregister
    login_valid = False
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == "POST":
        username = request.POST["username"]
        passw = request.POST["password"]
        user = authenticate(request, username=username, password=passw)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            isregister = False
            login_valid = True
            return render(request, 'authentication/login.html', {'isregister': isregister, 'login_valid': login_valid})
    return render(request, 'authentication/login.html', {'isregister': isregister, 'login_valid': login_valid})


def register(request):
    global isregister
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == "POST":
        username = request.POST["username"]
        request.session['username'] = username
        passw = request.POST["password"]
        user = User.objects.create_user(username, username, passw)
        user.save()
        name = request.POST['name']
        bio = request.POST['bio']
        email = request.POST['email']
        phoneno = request.POST['phonen']
        date = request.POST['bdate']
        pic = request.FILES.get('pic', False)
        pic.name = username+'.jpg'
        userData.objects.create(user_name=str(username), name=name, user_desc=bio,
                                user_email=email, user_phone=str(phoneno), user_birthday=date, user_pic=pic)
        isregister = True
        login(request, authenticate(username=username, password=passw))
        return redirect('/')

    else:
        isregister = False
        all_username = User.objects.all()
        all_username = [i.username for i in all_username]
        return render(request, 'authentication/register.html', {'all_username': json.dumps(all_username)})


@login_required(login_url='login')
def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "Logged out successfully")
        return redirect("/login")


@login_required(login_url='login')
def home(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    elif request.user.is_authenticated:
        username = request.user.username
        return render(request, 'baseTemplate.html', {'user_data': userObj(username), 'profile_pic': userObj(username)['user_pic']})


@login_required(login_url='login')
def profile(request, username):
    if not request.user.is_authenticated:
        return redirect('/login')
    elif username in User.objects.values_list('username', flat=True):
        userQuery = user_data.getUserModelInstance(username)
        authUserQuery = user_data.getUserModelInstance(request.user.username)
        post_data = post_util.get_post_data(username, include_likes=False)
        posts_length = len(post_data)
        if username == request.user.username:
            profile_pic = userObj(username)['user_pic']
        else:
            profile_pic = userObj(request.user.username)['user_pic']
        followers = userFollowers.objects.filter(follower=userQuery)
        following = userFollowers.objects.filter(following=userQuery)
        isAuthUserFollows = followers.filter(following=authUserQuery).exists()
        return render(request, 'profile/index.html', {'user_data': userObj(username), 'post_data': post_data, 'followers': [followers, following, isAuthUserFollows], 'post_length': str(posts_length), 'profile_pic': profile_pic, 'searchedUserPic': userObj(username)['user_pic']})
    else:
        return HttpResponse("404 not found")


@login_required(login_url='login')
@csrf_exempt
def edit_profile(request):
    if request.method == 'POST':
        if 'image' in request.FILES:
            from PIL import Image
            pic = request.FILES['image']
            Image.open(pic).save('media/' + pic.name)
            userData.objects.filter(
                user_name=request.user.username)
            userData.user_pic = pic
            userData.save()
        elif 'name' in request.POST:
            name = request.POST['name']
            bio = request.POST['bio']
            email = request.POST['email']
            phoneN = request.POST['phoneN']
            userData.objects.filter(user_name=request.user.username).update(
                name=name, user_desc=bio, user_email=email, user_phone=phoneN)
        return render(request, 'usersettings/editProfile.html', {'user_data': userObj(request.user.username), 'profile_pic':  userObj(request.user.username)['user_pic'], 'isupdate': True})
    return render(request, 'usersettings/editProfile.html', {'user_data':  userObj(request.user.username), 'profile_pic':  userObj(request.user.username)['user_pic'], 'isupdate': False})


def changePassword(request):
    if request.method == "POST":
        old_pass = request.POST['old_pass']
        new_pass = request.POST['new_pass']
        user = authenticate(
            request, username=request.user.username, password=old_pass)
        if user is not None:
            user.set_password(new_pass)
            user.save()
            return redirect('/login')
        else:
            return render(request, 'usersettings/changepassword.html', {'profile_pic': userObj(request.user.username)['user_pic'], 'ispassValid': True})
    return render(request, 'usersettings/changepassword.html', {'profile_pic': userObj(request.user.username)['user_pic'], 'ispassValid': False})


def chatTo(request, username):
    user2 = get_user_model().objects.get(username=username)
    print(userData.objects.get(user_name=request.user.username))
    Thread.objects.create(user1=request.user, user2=user2, user1_profile_pic=userData.objects.get(
        user_name=request.user.username), user2_profile_pic=userData.objects.get(user_name=username))
    return redirect('/chat/')


def Follow(request, username):

    if request.method == "POST":
        username = request.POST['data[user]']
        if username in User.objects.values_list('username', flat=True):
            user1 = userData.objects.get(user_name=request.user.username)
            user2 = userData.objects.get(user_name=username)
            if user1.user_name != user2.user_name:
                if userFollowers.objects.filter(following=user1, follower=user2).exists():
                    userFollowers.objects.filter(
                        following=user1, follower=user2).delete()
                    return HttpResponse("unfollow")
                else:
                    userFollowers.objects.create(
                        following=user1, follower=user2)
                    return HttpResponse("followed")
        else:
            return HttpResponse("404 not found")
    else:
        return HttpResponse("404 not found")


def SearchUser(request):
    username = request.GET.get('userName', '')
    usernames = ' '.join(username.lower().split()).split(' ')
    usersThreshold = 8
    response = []
    userAuthQuery = user_data.getUserModelInstance(request.user.username)
    # first check whether user have type more than 3 characters
    if len(username) > 3:
        for username in usernames:
            if len(username) > 3:
                all_users = userData.objects.filter(
                    Q(user_name__icontains=username) | Q(name__icontains=username)).exclude(user_name=request.user.username)
                for user in all_users:
                    tmpUserObj = userObj(user.user_name)
                    if tmpUserObj in response:
                        print("here ??")
                        continue
                    is_following = userFollowers.objects.filter(
                        following=userAuthQuery, follower=user).exists()
                    is_followed = userFollowers.objects.filter(
                        following=user, follower=userAuthQuery).exists()
                    if is_following or is_followed:
                        if is_following:
                            tmpUserObj['is_following'] = True
                        if is_followed:
                            tmpUserObj['is_followed'] = True
                        if tmpUserObj in response:
                            print("here ??")
                            continue
                        response.append(tmpUserObj)
                    else:
                        response.append(tmpUserObj)

            response = sorted(response, key=lambda user: (
                user['is_following'], user['is_followed']), reverse=True)[:usersThreshold]

        if len(response) == 0:
            response = "NoUserFound"

    else:
        response = "LessChar"
    return JsonResponse(response, safe=False)
