from posts.models import Post, Comment
from datetime import datetime, timezone

def get_feed_posts(users,feed_results,type):
    for user in users:
        if type == 'following':
            posts = Post.objects.filter(username=user.follower).order_by('-date_posted')
        elif type == 'followers':
            posts = Post.objects.filter(username=user.following).order_by('-date_posted')
        else:
            posts = Post.objects.filter(username=user).order_by('-date_posted')
        if posts.exists():
            # print([post.likes.count() + Comment.objects.filter(post=post).count() for post in posts])
            selected_post = max((
                (post,post.likes.count() + Comment.objects.filter(post=post).count())
                for post in posts
                if (datetime.now(timezone.utc) - post.date_posted).days <= 7),key=lambda x: x[1],default=None
            )
            if selected_post:feed_results.add(selected_post[0])

