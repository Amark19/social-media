from django.db import models
from django.contrib.auth import get_user_model
from user.models import userData
from datetime import datetime

User = get_user_model()



# Create your models here.
#why is it necesary to create a manager for the Thread model?
#because we want to create a custom method for the Thread model
#we want to create a method that will return all the threads that a user is involved in
class ThreadManager(models.Manager):
    def by_user(self,**kwargs):
        user = kwargs.get('user')
        return self.get_queryset().filter(models.Q(user1=user) | models.Q(user2=user)).distinct()#we r filtering the Thread queryset/all objects by the user1 or user2 field which helps us to filter threads by user

class Thread(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user1')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user2')
    user1_profile_pic = models.ForeignKey(userData, on_delete=models.CASCADE, related_name='thread_user1_profile_pic',null=True, blank=True)
    user2_profile_pic = models.ForeignKey(userData, on_delete=models.CASCADE, related_name='thread_user2_profile_pic', null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    objects  = ThreadManager() #now through objects we can access the by_user method

    class Meta:
        unique_together = ['user1', 'user2']

class ChatMessage(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name='chatmessage_thread')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(default=datetime.now)

    def formatted_date(self):
        return self.timestamp.strftime('%m/%d/%Y %I:%M %p')