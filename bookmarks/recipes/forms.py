from django import forms
from .models import Recipe, Article, RecipeComment, ArticleComment

class RecipeCreateForm(forms.ModelForm):
	class Meta:
		model = Recipe
		fields = ('title', 'picture', 'region', 'country', 'diet', 'prep_time', 'description', 'steps', 'ingredients')
		

class ArticleCreateForm(forms.ModelForm):
	class Meta:
		model = Article
		fields = ('title', 'category', 'picture', 'description')


class RecipeCommentForm(forms.ModelForm):
	class Meta:
		model = RecipeComment
		fields = ('body',)

class ArticleCommentForm(forms.ModelForm):
	class Meta:
		model = ArticleComment
		fields = ('body',)
		

