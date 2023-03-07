from ..models import Post

def get_post_data(username,include_likes=True):
    if include_likes:
        post_data = Post.objects.values(
            'post_id', 'content', 'date_posted', 'media', 'likes').filter(username=username)
    else:
        post_data = Post.objects.values(
            'post_id', 'content', 'date_posted', 'media').filter(username=username)
    return post_data