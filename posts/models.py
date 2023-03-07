from django.db import models
from django.contrib.auth.models import User
from user.models import userData
from django.utils import timezone

# create a new model for posts which will be linked to the user model


class Post(models.Model):
    post_id = models.AutoField(primary_key=True)
    content = models.TextField()
    date_posted = models.DateTimeField(editable=False)
    media = models.FileField(upload_to='media', blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=100, default="")
    likes = models.ManyToManyField(User, related_name="likes")# post can have many likes & each like is a user & each user can like many posts

    def save(self, *args, **kwargs):
        if not self.post_id:
            self.date_posted = timezone.now()
        return super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.user.username}_{self.post_id}'


class Comment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    comment = models.TextField(default="")
    created_date = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.user.username}_{self.post_id}'
