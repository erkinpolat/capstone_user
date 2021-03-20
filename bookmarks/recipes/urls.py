from django.urls import path 
from . import views

app_name = 'recipes'

urlpatterns = [
	path('create/<int:id>/<slug:slug>/', views.recipe_create, name='create'),
	path('cookbook/<int:id>/<slug:slug>/add_collaborator/', views.BootstrapFilterView, name='add_collaborator'),
	path('create_cookbook/', views.cookbook_create, name='cookbook_create'),
	path('create_article/', views.article_create, name='article_create'),
	path('detail/<int:id>/<slug:slug>/', views.recipe_detail, name='detail'),
	path('articles/<int:id>/<slug:slug>/', views.article_detail, name='article_detail'),
	path('', views.cookbook_list, name='cookbook_list'),
	path('cookbook/<int:id>/<slug:slug>/', views.cookbook_detail, name='cookbook_detail'),
	path('articles/', views.article_list, name='articles'),
	path('like/', views.recipe_like, name='like'),
	path('welcome/', views.mainpage, name='mainpage'),
	path('<slug:region_slug>/', views.recipe_list, name='recipes_by_region'),
	path('articles/<slug:category_slug>/', views.article_list, name='articles_by_category'),
	path('about', views.about, name='about'),
]



#path('', views.recipe_list, name='list'),