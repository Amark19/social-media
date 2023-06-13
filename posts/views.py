from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
from .models import Post, Comment
from user.models import userData
import json
from datetime import datetime, timezone
from django.core import serializers
from .utils import time_diff
from user.utils import user_data


def get_comments_data(all_comments):
    all_comments = all_comments.order_by('-created_date').all()
    comments_data = []
    for i in range(len(all_comments)):
        comments_data.append({
            'comment': all_comments[i].comment,
            'created_date': all_comments[i].created_date,
            'user_name': all_comments[i].user.username,
            'user_pic':userData.objects.get(user_name=all_comments[i].user.username).user_pic.url,
            'time_ago': time_diff.time_diff(datetime.now(timezone.utc), all_comments[i].created_date)
        })
    return comments_data


@login_required(login_url='login')
def create_post(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        media = request.FILES.get('media', False)
        compressed_media = user_data.compress_and_save_image(media)
        post = Post(content=content, user=request.user, username=request.user.username)
        post.media.save(media.name, compressed_media)
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
        elif update_type == 'caption':
            content = request.POST['data[caption]']
            post.content = content
            post.save()
            return JsonResponse({'caption':content}, safe=False)
    return HttpResponse("There is nothing to show here ...")


@login_required(login_url='login')
def view_post(request, post_id):
    post = Post.objects.get(post_id=post_id)
    userObj = userData.objects.get(user_name=post.username)
    post_json = serializers.serialize(
        'json', [post,])
    if post.likes.filter(id=request.user.id).exists():
        is_like = 1
    else:
        is_like = 0
    profile_pic = userData.objects.get(user_name=request.user.username).user_pic
    return render(request, 'viewPost.html', {'post': post, 'post_json': post_json, 'user_data': userObj, 'profile_pic': profile_pic, 'is_like': is_like, 'comments_data': get_comments_data(Comment.objects.filter(post=post).all())})


@login_required(login_url='login')
def delete_post(request, post_id):
    post = Post.objects.get(post_id=post_id)
    post.delete()
    default_storage.delete(post.media.name)
    return redirect(f'/{request.user}/')