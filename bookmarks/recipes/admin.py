from django.contrib import admin
from .models import Recipe, Diet, Region, Article, Category, RecipeComment, ArticleComment
# Register your models here.

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
	list_display = ['title', 'slug', 'picture', 'created', 'diet', 'region', 'prep_time']
	list_filter = ['created']

@admin.register(Diet)
class DietAdmin(admin.ModelAdmin):
	list_display = ['name', 'slug']

@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
	list_display = ['name', 'slug']

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
	list_display = ['title', 'user', 'slug', 'created']
	list_filter = ['created']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	list_display = ['name', 'slug']

@admin.register(RecipeComment)
class RecipeCommentAdmin(admin.ModelAdmin):
	list_display = ['user', 'post', 'created']

@admin.register(ArticleComment)
class ArticleCommentAdmin(admin.ModelAdmin):
	list_display = ['user', 'post', 'created']