from ..models import Post

def get_post_data(r):
    post_data = Post.objects.values(
        'post_id', 'content', 'date_posted', 'media', 'likes').filter(user=r.user)
    return post_data