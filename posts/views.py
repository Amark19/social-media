from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Post
from user.models import userData


def get_user_data(r):
    global user_data
    user_data = userData.objects.values(
        'name', 'user_desc', 'user_email', 'user_phone', 'user_birthday', 'user_pic').filter(user_name=r.user.username)
    return user_data


@login_required(login_url='login')
def create_post(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        media = request.FILES.get('media', False)
        post = Post(content=content, media=media, user=request.user)
        post.save()
        return redirect(f'/{request.user}/')

@login_required(login_url='login')
def view_post(request, post_id):
    post = Post.objects.get(post_id=post_id)
    return render(request, 'viewPost.html', {'post': post, 'user_data': get_user_data(request)})
