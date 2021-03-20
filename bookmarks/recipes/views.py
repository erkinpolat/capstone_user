from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RecipeCreateForm, ArticleCreateForm, CookBookCreateForm, RecipeCommentForm, ArticleCommentForm
from .models import Recipe, Diet, Region, Article, Category, CookBook
from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.views.decorators.http import require_POST
from common.decorators import ajax_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.urls import reverse
from django.contrib.auth import get_user_model




# Create your views here.
@login_required
def recipe_create(request, id, slug):
	'''
	Function to create recipes for a given CookBook. If request is GET, displays the form. If the request is POST creates the new recipe
	with the data received from the RecipeCreateForm

	Args:
		id: The id of the CookBook the recipe will be associated with
		slug: The slug of the CookBook

	Returns:
		Either the rendered template for the empty recipe creation form or the page for the newly created recipe based on the type of the request
	'''
	if request.method == 'POST':
		form = RecipeCreateForm(data = request.POST, files=request.FILES)
		if form.is_valid():
			#cd = form.cleaned_data
			new_item = form.save(commit=False)

			new_item.user = request.user

			cookbook = get_object_or_404(CookBook, id=id, slug=slug)
			new_item.cookbook = cookbook
			new_item.save()

			#messages.success(request, 'Recipe added successfully')

			return redirect(new_item.get_absolute_url())
	else:
		form = RecipeCreateForm()

	return render(request, 'recipes/recipe/create.html', {'section': 'recipes', 'form': form})

@login_required
def article_create(request):
	'''
	Function to create new articles. Unlike recipes, the articles don't need to be associated with any other object.
	with the data received from the ArticleCreateForm

	Args:
		request

	Returns:
		The empty article creation form if the request is GET, or the newly created article if the request is POST
	'''
	if request.method == 'POST':
		form = ArticleCreateForm(data = request.POST, files=request.FILES)
		if form.is_valid():
			new_item = form.save(commit=False)
			new_item.user = request.user
			new_item.save()

			return redirect(new_item.get_absolute_url())
	else:
		form = ArticleCreateForm()

	return render(request, 'recipes/recipe/article_create.html', {'form': form})

@login_required
def cookbook_create(request):
	'''
	Function to create new CookBooks with the data received from the CookBookCreateForm upon POSt request.

	Args:
		request

	Returns:
		The empty CookBook creation form if the request is GET, or the newly created CookBook if the request is POST
	'''
	if request.method == 'POST':
		form = CookBookCreateForm(data = request.POST, files=request.FILES)
		if form.is_valid():
			#cd = form.cleaned_data
			new_item = form.save(commit=False)

			new_item.user = request.user

			new_item.save()
			new_item.collaborators.add(request.user)
			new_item.save()

			#messages.success(request, 'Recipe added successfully')

			return redirect(new_item.get_absolute_url())
	else:
		form = CookBookCreateForm()

	return render(request, 'recipes/recipe/cookbook_create.html', {'section': 'recipes', 'form': form})

def recipe_detail(request, id, slug):
	'''
	Function to display a single recipe. If the method is GET, just gets the recipe and all the likes and comments associated with it.
	If the method is saves the like or the comment in the database based on the name of the request.

	Receives the comment data from the POST['comment'] and receives the like information from POST['title'] 

	Args:
		request
		id: Id of the recipe to be displayed
		slug: Slug of the recipe to be displayed
	Returns:
		Template to be rendered for a given recipe 
	'''
	recipe = get_object_or_404(Recipe, id=id, slug=slug)
	comments = recipe.comments.all()	
	ingredients = recipe.ingredients.splitlines()
	steps = recipe.steps.splitlines()
	diet = str(recipe.diet)
	new_comment = None

	if request.method == "POST" and 'title' in request.POST:
		
		action = request.POST.get('title')

		if action:
			if action == 'like':
				recipe.users_like.add(request.user)
			else:
				recipe.users_like.remove(request.user)

		return HttpResponseRedirect(reverse('recipes:detail', args=[id, slug]))
		

	if request.method == "POST" and 'comment' in request.POST:
		comment_form = RecipeCommentForm(data=request.POST)
		if comment_form.is_valid():
			#Create comment but don't save it
			new_comment = comment_form.save(commit = False)
			#The post is assigned to the comment
			new_comment.post = recipe
			new_comment.user = request.user
			#save to the database
			new_comment.save()

		return HttpResponseRedirect(reverse('recipes:detail', args=[id, slug]))

	else:
		comment_form = RecipeCommentForm()	
	

	return render(request, 'recipes/recipe/article.html', {'section': 'recipes', 'recipe': recipe, 'ingredients': ingredients, 'steps': steps, 'diet': diet, 'comments': comments, 'comment_form': comment_form})

def article_detail(request, id, slug):
	'''
	Function to display a single article. If the method is GET, just gets the article and all the likes and comments associated with it.
	If the method is saves the like or the comment in the database based on the name of the request.

	Receives the comment data from the POST['comment'] and receives the like information from POST['title'] 

	Args:
		request
		id: Id of the article to be displayed
		slug: Slug of the article to be displayed
	Returns:
		Template to be rendered for a given article 
	'''

	article = get_object_or_404(Article, id=id, slug=slug)
	comments = article.comments.all()
	new_comment = None


	if request.method == "POST" and 'title' in request.POST:
		
		action = request.POST.get('title')

		if action:
			if action == 'like':
				article.users_like.add(request.user)
			else:
				article.users_like.remove(request.user)

		return HttpResponseRedirect(reverse('recipes:article_detail', args=[id, slug]))
		

	if request.method == "POST" and 'comment' in request.POST:
		comment_form = ArticleCommentForm(data=request.POST)
		if comment_form.is_valid():
			#Create comment but don't save it
			new_comment = comment_form.save(commit = False)
			#The post is assigned to the comment
			new_comment.post = article
			new_comment.user = request.user
			#save to the database
			new_comment.save()

		return HttpResponseRedirect(reverse('recipes:article_detail', args=[id, slug]))

	else:
		comment_form = ArticleCommentForm()

	return render(request, 'recipes/recipe/nonrecipearticle.html', {'section': 'recipes', 'article': article, 'comments': comments, 'comment_form': comment_form})


def cookbook_detail(request, id, slug):
	'''
	Function to display a cookbook nad all the recipes associated with it. Gets all the recipes and the collaborators from the database.
	

	Args:
		request
		id: Id of the CookBook to be displayed
		slug: Slug of the CookBook to be displayed
	Returns:
		Template to be rendered for a given CookBook 
	'''
	cookbook = get_object_or_404(CookBook, id=id, slug=slug)

	recipes = cookbook.recipes_in_cookbook.all()
	collaborators = cookbook.collaborators.all()

	print(collaborators)

	return render(request, 'recipes/recipe/cookbook_detail.html', {'section': 'recipes', 'cookbook': cookbook, 'recipes': recipes, 'collaborators': collaborators})


@ajax_required
@login_required
@require_POST
def recipe_like(request):
	'''
	Function to handle the Ajax when a user likes a recipe or an article. 
	'''
	recipe_id = request.POST.get('id')
	action = request.POST.get('action')
	if recipe_id and action:
		try:
			recipe = Recipe.objects.get(id=recipe_id)
			if action == 'like':
				recipe.users_like.add(request.user)
			else:
				recipe.users_like.remove(request.user)
			return JsonResponse({'status': 'ok'})
		except:
			pass
	return JsonResponse({'status': 'error'})


def mainpage(request):
	'''
	Function to handle the view for the mainpage. Gets the latest 6 recipes and 6 articles and renders the template for the mainpage.
	'''
	recipes = Recipe.objects.order_by('-created')[:6]
	articles = Article.objects.order_by('-created')[:6]
	return render(request, 'recipes/recipe/mainpage.html', {'recipes': recipes, 'articles': articles})

def cookbook_list(request):
	'''
	View function to handle the list of CookBooks. Is called from the url for the view of all CookBooks. Also uses the searchbar.
	If the user typed something in the searchbar, the data GET['q'] from GET request is passed into the get_query_set() function 
	to get a custom query.

	Args:
		request
	Returns:
		Rendered template for all of the queried CookBooks
	'''
	query=""

	if request.GET:
		query = request.GET['q']
		cookbooks = get_query_set(CookBook, str(query))
	else:
		cookbooks = CookBook.objects.all()


	regions = Region.objects.all()

	paginator = Paginator(cookbooks, 6)
	page = request.GET.get('page')
	try:
		cookbooks = paginator.page(page)
	except PageNotAnInteger:
		cookbooks = paginator.page(1)
	except EmptyPage:
		#if the response is ajax don't do anything
		if request.is_ajax():
			return HttpResponse('')
		#if page is out of range deliver last page of results
		cookbooks = paginator.page(paginator.num_pages)
	if request.is_ajax():
		return render(request, 'recipes/recipe/list_ajax.html', {'section': 'recipes', 'cookbooks': cookbooks, 'browse': regions, 'browse_key': "Region"})
	return render(request, 'recipes/recipe/list.html', {'section': 'recipes', 'cookbooks': cookbooks, 'browse': regions, 'browse_key': "Region"})





def recipe_list(request, region_slug=False):
	'''
	View function to handle the list of recipes. Is called from the url for the view of all recipes. Also uses the searchbar.
	If the user typed something in the searchbar, the the data GET['q'] from GET request is passed into the get_query_set() function 
	to get a custom query.
	Also, filters the recipes based on the region if a region slug is provided by the user.

	Args:
		request
		region_slug: slug representing a region. Passed through a button
	Returns:
		Rendered template for all of the queried recipes
	'''
	query=""

	if request.GET:
		query = request.GET['q']
		recipes = get_query_set(Recipe, str(query))
	else:
		recipes = Recipe.objects.all()
		if region_slug:
			recipes = recipes.filter(region__slug=region_slug)

	regions = Region.objects.all()

	

	
	paginator = Paginator(recipes, 6)
	page = request.GET.get('page')
	try:
		recipes = paginator.page(page)
	except PageNotAnInteger:
		recipes = paginator.page(1)
	except EmptyPage:
		#if the response is ajax don't do anything
		if request.is_ajax():
			return HttpResponse('')
		#if page is out of range deliver last page of results
		recipes = paginator.page(paginator.num_pages)
	if request.is_ajax():
		return render(request, 'recipes/recipe/list_ajax.html', {'section': 'recipes', 'recipes': recipes, 'browse': regions, 'browse_key': "Region"})
	return render(request, 'recipes/recipe/list.html', {'section': 'recipes', 'recipes': recipes, 'browse': regions, 'browse_key': "Region"})

def article_list(request, category_slug=False):
	'''
	View function to handle the list of articles. Is called from the url for the view of all articles. Also uses the searchbar.
	If the user typed something in the searchbar, the data GET['q'] from GET request is passed into the get_query_set() function 
	to get a custom query.
	Also, filters the articles based on the category if a category slug is provided by the user.

	Args:
		request
		category_slug: slug representing a region. Passed through a button
	Returns:
		Rendered template for all of the queried articles
	'''


	query=""

	if request.GET:
		query = request.GET['q']
		articles = get_query_set(Article, str(query))
	else:	
		articles = Article.objects.all()
		if category_slug:
			articles = articles.filter(category__slug=category_slug)

	categories = Category.objects.all()

	

	paginator = Paginator(articles, 6)
	page = request.GET.get('page')
	try:
		articles = paginator.page(page)
	except PageNotAnInteger:
		articles = paginator.page(1)
	except EmptyPage:
		#if the response is ajax don't do anything
		if request.is_ajax():
			return HttpResponse('')
		#if page is out of range deliver last page of results
		articles = paginator.page(paginator.num_pages)
	if request.is_ajax():
		return render(request, 'recipes/recipe/list_ajax.html', {'section': 'articles', 'recipes': articles, 'browse': categories, 'browse_key': "Category"})
	return render(request, 'recipes/recipe/list.html', {'section': 'articles', 'recipes': articles, 'browse': categories, 'browse_key': "Category"})

def get_query_set(model, query=None):
	'''
	Function to run queries on any article/recipe/CookBook object. Splits the query into words and searches the title and the descriptions of the  given model 
	by using each of these keywords.

	Args:
		model: Which model the search will be performed on
		query: String to be queried

	Returns:
		A query of model instances filtered for the search criteria
	'''
	queryset = []
	queries = query.split(" ")
	for q in queries:
		posts = model.objects.filter(
				Q(title__icontains=q) |
				Q(description__icontains=q)
			).distinct()

		for post in posts:
			queryset.append(post)

	return list(set(queryset))

@login_required
def BootstrapFilterView(request, id, slug):
	'''
	Function to handle searching of users and add them as a colaborator to the CookBook. If the request is GET, searches all of the users
	names, surnames and usernames for compatible matches and returns a list of queried users. The data is passed through GET['title_contains']
	If the request is POST, adds a given user to the list of collaborators for  that recipe.

	Args:
		request
		id: CookBook id
		slug: CookBook slug
	
	Returns:
		Either the rendered template contatining a list of users or redirects back to the CookBook page after adding the collaborator.
	'''
	cookbook = get_object_or_404(CookBook, id=id, slug=slug)
	collaborators = cookbook.collaborators.all()
	
	if request.GET:
		title_contains = request.GET.get('title_contains')
		queries = title_contains.split(" ")

		queryset=[]

		User = get_user_model()

		users = User.objects.all()

		for q in queries:
			posts = User.objects.filter(Q(username__icontains=q) | Q(first_name__icontains=q) | Q(last_name__icontains=q)).distinct()

			for post in posts:
				if post not in collaborators:
					queryset.append(post)



		return render(request, "recipes/recipe/collaborator_form.html", {'users': queryset})

	elif request.POST:
		user_id = request.POST.get('add_user')

		User = get_user_model()
		user = User.objects.filter(id=user_id)[0]

		cookbook.collaborators.add(user)

		

		return HttpResponseRedirect(reverse('recipes:cookbook_detail', args=[id, slug]))



	return render(request, "recipes/recipe/collaborator_form.html", {})


def about(request):
	'''
	Function to handle the static about page. 
	'''
	return render(request, "recipes/recipe/about.html", {})


