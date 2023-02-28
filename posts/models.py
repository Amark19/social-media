from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# create a new model for posts which will be linked to the user model
class Post(models.Model):
    post_id = models.AutoField(primary_key=True)
    content = models.TextField()
    date_posted = models.DateTimeField(editable=False)
    media = models.FileField(upload_to='media', blank=True)
    comments = models.TextField(blank=True)
    likes = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.post_id:
            self.date_posted = timezone.now()
        return super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.user.username}_{self.post_id}'