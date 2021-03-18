from django.contrib.auth import get_user_model
from django.conf import settings
from django.db import models
from recipes.models import CookBook
from django.urls import reverse

# Create your models here.

User = get_user_model()
DEFAULT_CHAT_ID = 1


class Message(models.Model):
	author = models.ForeignKey(User, related_name='author_messages', on_delete = models.CASCADE)
	content = models.TextField()
	timestamp = models.DateTimeField(auto_now_add=True)
	chat = models.ForeignKey('Chat', related_name='messages_in_chat', on_delete = models.CASCADE, default =1)

	def __str__(self):
		return self.author.username

	def last_10_messages(self):
		return Message.objects.order_by('-timestamp').all()[:10]

class Chat(models.Model):
	users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='users_chats', blank=True)
	description = models.TextField()
	cookbook = models.OneToOneField(CookBook, related_name='related_chat', on_delete = models.CASCADE)

	def get_absolute_url(self):
		return reverse('chat:messages_id', args=[self.id])
