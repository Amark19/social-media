from django.db import models

# Create your models here.
class userData(models.Model):
    user_name = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    user_email = models.CharField(max_length=30)
    user_desc = models.CharField(max_length=500)
    user_phone = models.CharField(max_length=30)
    user_birthday = models.DateField()
    user_pic = models.ImageField(upload_to='images',blank=True)
    def __str__(self):
        return self.user_name