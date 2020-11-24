from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RecipeCreateForm
from .models import Recipe
from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from common.decorators import ajax_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

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

def recipe_detail(request, id, slug):
	recipe = get_object_or_404(Recipe, id=id, slug=slug)
	return render(request, 'recipes/recipe/detail.html', {'section': 'recipes', 'recipe': recipe})

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
	return render(request, 'recipes/recipe/mainpage.html')

@login_required
def recipe_list(request):
	recipes = Recipe.objects.all()
	paginator = Paginator(recipes, 8)
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
		return render(request, 'recipes/recipe/list_ajax.html', {'section': 'recipes', 'recipes': recipes})
	return render(request, 'recipes/recipe/list.html', {'section': 'recipes', 'recipes': recipes})
