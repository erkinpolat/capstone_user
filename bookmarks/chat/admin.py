from django.contrib import admin
from .models import Message, Chat

# Register your models here.

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
	list_display = ['author', 'content', 'timestamp', 'chat']
	list_filter = ['chat', 'author', 'timestamp']


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
	list_display = ['description', 'cookbook']
	list_filter = ['cookbook', 'users']