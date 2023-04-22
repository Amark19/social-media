from django.contrib import admin
from .models import Thread, ChatMessage

# Register your models here.
admin.site.register(ChatMessage)


class ChatMessage(admin.TabularInline):
    model = ChatMessage


'''
A custom admin configuration is defined for the Thread model using a ThreadAdmin class. The inlines attribute is used to specify that when viewing a Thread in the admin interface, you can also see and edit its related ChatMessage objects inline. This means you can add, edit, or delete ChatMessage objects directly from the Thread change page.

Finally, the Meta class is used to specify the model that this admin configuration applies to.
'''
class ThreadAdmin(admin.ModelAdmin):
    inlines = [ChatMessage]

    class Meta:
        model = Thread

admin.site.register(Thread,ThreadAdmin)