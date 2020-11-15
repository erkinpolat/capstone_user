from django.contrib import admin
from .models import Recipe
# Register your models here.

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
	list_display = ['title', 'slug', 'picture', 'created']
	list_filter = ['created']

