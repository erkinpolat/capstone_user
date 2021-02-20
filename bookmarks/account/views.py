from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.contrib.auth import authenticate, login
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.contrib.auth import get_user_model
from recipes.models import Recipe, Article, CookBook
from common.decorators import ajax_required
from django.views.decorators.http import require_POST
from django.db.models import Q

# Create your views here.

User = get_user_model()

@login_required
def dashboard(request):
	profile = get_object_or_404(Profile, user=request.user)
	return render(request, 'account/dashboard.html', {'section': 'dashboard', 'profile': 'profile'})

@login_required
def profile(request):
	profile = get_object_or_404(Profile, user=request.user)
	recipes = get_user_objects(user=request.user, model=Recipe)
	cookbooks = request.user.cookbooks_collaborating.all()
	articles = get_user_objects(user=request.user, model=Article)
	following = request.user.following.all()
	return render(request, 'account/profile.html', {'section': 'profile', 'cookbooks': cookbooks, 'recipes': recipes, 'articles': articles, 'following': following})


def other_profile(request, user_id):
	if request.user.id == user_id:
		user = get_object_or_404(User, id = user_id)
		cookbooks = user.cookbooks_collaborating.all()
		recipes = get_user_objects(user=user, model=Recipe)
		articles = get_user_objects(user=user, model=Article)
		following = user.following.all()
		return render(request, 'account/profile.html', {'section': 'profile', 'cookbooks': cookbooks, 'recipes': recipes, 'articles': articles, 'following': following})
	else:
		if request.method == "POST":
			user = get_object_or_404(User, id = user_id)
			cookbooks = user.cookbooks_collaborating.all()
			recipes = get_user_objects(user=user, model=Recipe)
			articles = get_user_objects(user=user, model=Article)
			following = user.following.all()

			action = request.POST.get('title')
			print(action)
			if action:
				followed_user = user.profile
				if action == 'follow':
					followed_user.followers.add(request.user)
				else:
					followed_user.followers.remove(request.user)
				return render(request, 'account/generic_profile.html', {'section': 'profile', 'cookbooks': cookbooks, 'user': user, 'recipes': recipes, 'articles': articles, 'following': following})

		else:
		
			user = get_object_or_404(User, id = user_id)
			cookbooks = user.cookbooks_collaborating.all()
			recipes = get_user_objects(user=user, model=Recipe)
			articles = get_user_objects(user=user, model=Article)
			following = user.following.all()
			return render(request, 'account/generic_profile.html', {'section': 'profile', 'cookbooks': cookbooks, 'user': user, 'recipes': recipes, 'articles': articles, 'following': following})


'''@login_required
@require_POST
def follow_user(request):
	if request.POST():
		user_id = request.POST.get('id')
		action = request.POST.get('action')
		if user_id and action:
			try:
				followed_user = Profile.objects.get(user__id=user_id)
				if action == 'follow':
					followed_user.followers.add(request.user)
				else:
					followed_user.followers.remove(request.user)
				print(success)
			except:
				print("error")'''



def user_login(request):
	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			user = authenticate(request, username=cd['username'], password=cd['password'])
			if user is not None:
				if user.is_active:
					login(request, user)
					return HttpResponse('Authenticated successfully')
				else:
					return HttpResponse('Disabled account')
			else:
				return HttpResponse('Invalid login')
	else:
		form = LoginForm()
	return render(request, 'account/login.html', {'form': form})

def register(request):
	if request.method == 'POST':
		user_form = UserRegistrationForm(request.POST)
		if user_form.is_valid():
			#Creating a new user without saving it
			new_user = user_form.save(commit=False)
			#set the password
			new_user.set_password(user_form.cleaned_data['password'])
			#save the user
			new_user.save()
			#Create user profile
			Profile.objects.create(user=new_user)
			user_profile = get_object_or_404(Profile, user = new_user)
			user_profile.photo = "users/generic/blank-profile-picture-973460_640.png"
			user_profile.save()

			return render(request, 'account/register_done.html', {'new_user': new_user})
	else:
		user_form = UserRegistrationForm()
	return render(request, 'account/register.html', {'user_form': user_form})

@login_required
def edit(request):
	if request.method == 'POST':
		user_form = UserEditForm(instance=request.user, data=request.POST)
		profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
		if user_form.is_valid() and profile_form.is_valid():
			user_form.save()
			profile_form.save()

	else:
		user_form = UserEditForm(instance=request.user)
		profile_form = ProfileEditForm(instance=request.user.profile)

	return render(request, 'account/edit.html', {'user_form': user_form, 'profile_form': profile_form})


def get_user_objects(user, model):
	try:
		objects = get_list_or_404(model, user=user)
	except:
		objects = []
	return objects


@login_required
def messages(request):
	return render(request, 'account/messages.html', {})

def user_search(request):
	if request.GET:
		search = request.GET.get('query')
		queries = search.split(" ")

		queryset=[]

		User = get_user_model()

		users = User.objects.all()

		for q in queries:
			matching_users = User.objects.filter(Q(username__icontains=q) | Q(first_name__icontains=q) | Q(last_name__icontains=q)).distinct()

			for post in matching_users:
				if post.id != request.user.id:
					queryset.append(post)

		return render(request, 'account/user_search.html', {'queryset': queryset})

	return render(request, 'account/user_search.html', {})
