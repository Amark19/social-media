from posts.models import Post, Comment
from datetime import datetime, timezone
from user.utils import user_data
from posts.utils import time_diff

def get_feed_posts(users,feed_results,type):
    for user in users:
        if type == 'following':
            posts = Post.objects.filter(username=user.follower).order_by('-date_posted')
        elif type == 'followers':
            posts = Post.objects.filter(username=user.following).order_by('-date_posted')
        else:
            posts = Post.objects.filter(username=user).order_by('-date_posted')
        if posts.exists():
            selected_post = max((
                (post,post.likes.count() + Comment.objects.filter(post=post).count())
                for post in posts
                if (datetime.now(timezone.utc) - post.date_posted).days <= 30),key=lambda x: x[1],default=None
            )
            if selected_post:feed_results.append(selected_post[0])


def manage_feed(feed_results):
    feed_response = []
    for post in feed_results:
        post_userInstace = user_data.getUserModelInstance(post.username)
        feed_response.append({
            'post_id': post.post_id,
            'media': post.media.url,
            'caption': post.content,
            'likes': post.likes.count(),
            'comments': Comment.objects.filter(post=post).count(),
            'user_name': post.username,
            'name': post_userInstace.name,
            'user_pic': post_userInstace.user_pic.url,
            'post_time': time_diff.time_diff(datetime.now(timezone.utc),post.date_posted)
        })
    return feed_response