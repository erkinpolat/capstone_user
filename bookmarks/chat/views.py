from django.shortcuts import render, redirect
from .models import Message, Chat
from django.shortcuts import get_object_or_404

# Create your views here.

def index(request):
	return render(request, 'index.html', {})

def room(request, room_name):
	return render(request, 'room.html', {
		'room_name': room_name
	})

def messages(request, id=None):
	conversations = request.user.users_chats.all()

	if id:
		chat = get_object_or_404(Chat, id=id)

	else:
		chat = conversations[0]

	messages = chat.messages_in_chat.all()

	if request.method == "POST":
		action = request.POST.get("message_content")
		user = request.user

		new_message = Message(author=user, content=action, chat=chat)
		new_message.save()

		return redirect(chat.get_absolute_url())


	return render(request, 'messages.html', {'conversations': conversations, 'chat': chat, 'messages': messages})