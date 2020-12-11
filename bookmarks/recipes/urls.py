from django.urls import path 
from . import views

app_name = 'recipes'

urlpatterns = [
	path('create/', views.recipe_create, name='create'),
	path('create_article/', views.article_create, name='article_create'),
	path('detail/<int:id>/<slug:slug>/', views.recipe_detail, name='detail'),
	path('articles/<int:id>/<slug:slug>/', views.article_detail, name='article_detail'),
	path('', views.recipe_list, name='list'),
	path('articles/', views.article_list, name='articles'),
	path('like/', views.recipe_like, name='like'),
	path('welcome/', views.mainpage, name='mainpage'),
	path('<slug:region_slug>/', views.recipe_list, name='recipes_by_region'),
	path('articles/<slug:category_slug>/', views.article_list, name='articles_by_category'),
]