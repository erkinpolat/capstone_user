from django.urls import path 
from . import views

app_name = 'recipes'

urlpatterns = [
	path('create/', views.recipe_create, name='create'),
	path('detail/<int:id>/<slug:slug>/', views.recipe_detail, name='detail'),
	path('', views.recipe_list, name='list'),
	path('like/', views.recipe_like, name='like'),
	path('welcome/', views.mainpage, name='mainpage'),
]