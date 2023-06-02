from django.contrib import admin
from .models import userData, userFollowers

# Register your models here.
admin.site.register(userData)
admin.site.register(userFollowers)