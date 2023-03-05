from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Post, Comment
from user.models import userData
import json
from datetime import datetime, timezone
from django.core import serializers
from .utils import time_diff


def get_user_data(r):
    global user_data
    user_data = userData.objects.values(
        'name', 'user_desc', 'user_email', 'user_phone', 'user_birthday', 'user_pic').filter(user_name=r.user.username)
    return user_data


def get_comments_data(all_comments):
    comments_data = []
    for i in range(len(all_comments)):
        comments_data.append({
            'comment': all_comments[i].comment,
            'created_date': all_comments[i].created_date,
            'user_name': all_comments[i].user.username,
            'user_pic': userData.objects.values('user_pic').filter(user_name=all_comments[i].user.username)[0]['user_pic'],
            'time_ago': time_diff.time_diff(datetime.now(timezone.utc), all_comments[i].created_date)
        })
    # sorting comments by time_ago
    
    return comments_data


@login_required(login_url='login')
def create_post(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        media = request.FILES.get('media', False)
        post = Post(content=content, media=media, user=request.user)
        post.save()
        return redirect(f'/{request.user}/')


@login_required(login_url='login')
def update_post(request):
    if request.method == "POST":
        post_id, update_type = request.POST['data[post_id]'], request.POST['data[update_type]']
        post = Post.objects.get(post_id=post_id)
        if update_type == 'like':
            if post.likes.filter(id=request.user.id).exists():
                is_like = 1
                post.likes.remove(request.user)
            else:
                is_like = 0
                post.likes.add(request.user)
            return JsonResponse({'is_like': is_like, 'likes_count': post.likes.count()}, safe=False)
        elif update_type == 'comment':
            comment = request.POST['data[comment]']
            Comment(user=request.user, post=post, comment=comment,
                    created_date=datetime.now(timezone.utc)).save()
            return JsonResponse(get_comments_data(Comment.objects.filter(post=post).all()), safe=False)
        post.save()
    return HttpResponse("There is nothing to show here ...")


@login_required(login_url='login')
def view_post(request, post_id):
    post = Post.objects.get(post_id=post_id)
    post_json = serializers.serialize(
        'json', [post,])
    if post.likes.filter(id=request.user.id).exists():
        is_like = 1
    else:
        is_like = 0
    return render(request, 'viewPost.html', {'post': post, 'post_json': post_json, 'user_data': get_user_data(request),'is_like':is_like,'comments_data': get_comments_data(Comment.objects.filter(post=post).all())})
