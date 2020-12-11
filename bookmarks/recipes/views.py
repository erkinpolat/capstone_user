from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RecipeCreateForm, ArticleCreateForm, RecipeCommentForm, ArticleCommentForm
from .models import Recipe, Diet, Region, Article, Category
from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.views.decorators.http import require_POST
from common.decorators import ajax_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.urls import reverse


# Create your views here.
@login_required
def recipe_create(request):
	if request.method == 'POST':
		form = RecipeCreateForm(data = request.POST, files=request.FILES)
		if form.is_valid():
			#cd = form.cleaned_data
			new_item = form.save(commit=False)

			new_item.user = request.user
			new_item.save()

			#messages.success(request, 'Recipe added successfully')

			return redirect(new_item.get_absolute_url())
	else:
		form = RecipeCreateForm()

	return render(request, 'recipes/recipe/create.html', {'section': 'recipes', 'form': form})

@login_required
def article_create(request):
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

def recipe_detail(request, id, slug):
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



class PostListView(ListView):
	queryset = Recipe.objects.all()
	context_object_name = 'recipes'
	paginate_by = 3
	template_name = 'recipes/recipe/list.html'

@ajax_required
@login_required
@require_POST
def recipe_like(request):
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
	recipes = Recipe.objects.order_by('-created')[:6]
	articles = Article.objects.order_by('-created')[:6]
	return render(request, 'recipes/recipe/mainpage.html', {'recipes': recipes, 'articles': articles})


def recipe_list(request, region_slug=False):

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


