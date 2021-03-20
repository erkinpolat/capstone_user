from django.shortcuts import render, redirect
from .models import Message, Chat
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def messages(request, id=None):
	'''
	function to display the messages page. Gets post requests to send messages by writing the m in the database.

	Args:
		request
		id: id of the chat

	Returns: 
		renders the messages.html file with a given chat context
	'''

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