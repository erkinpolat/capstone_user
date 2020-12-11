from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.urls import reverse
from ckeditor.fields import RichTextField
# Create your models here.

class Recipe(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='recipes_created', on_delete=models.CASCADE)
	title = models.CharField(max_length = 200)
	slug = models.SlugField(max_length=200, blank=True)
	picture = models.ImageField(upload_to='recipes/%Y/%m/%d/', blank=True)
	region = models.ForeignKey('Region', related_name='recipes_from_region', on_delete=models.SET('None'))
	country = models.CharField(max_length = 200)
	diet = models.ForeignKey('Diet', related_name='recipes_in_diet', on_delete=models.SET('None'))
	prep_time = models.IntegerField()
	description = RichTextField()
	steps = models.TextField()
	ingredients = models.TextField()
	created = models.DateField(auto_now_add=True, db_index=True)
	users_like = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='recipes_liked', blank=True)

	def __str__(self):
		return self.title

	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = slugify(self.title)
		super().save(*args, **kwargs)

	def get_absolute_url(self):
		return reverse('recipes:detail', args=[self.id, self.slug])



class Diet(models.Model):
	name = models.CharField(max_length = 30)
	slug = models.SlugField(max_length=200, blank=True)


	def __str__(self):
		return self.name

	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = slugify(self.name)
		super().save(*args, **kwargs)

class Region(models.Model):
	name = models.CharField(max_length = 30)
	slug = models.SlugField(max_length=200, blank=True)

	def __str__(self):
		return self.name

	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = slugify(self.name)
		super().save(*args, **kwargs)

	def get_absolute_url(self):
		return f"/recipes/{self.slug}/"

class Article(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='articles_created', on_delete=models.CASCADE)
	title = models.CharField(max_length = 200)
	slug = models.SlugField(max_length=200, blank=True)
	category = models.ForeignKey('Category', related_name='articles_in_category', on_delete=models.SET('Other'))
	picture = models.ImageField(upload_to='recipes/%Y/%m/%d/', blank=True)
	description = RichTextField()
	created = models.DateField(auto_now_add=True, db_index=True)
	users_like = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='articles_liked', blank=True)

	def __str__(self):
		return self.title

	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = slugify(self.title)
		super().save(*args, **kwargs)

	def get_absolute_url(self):
		return reverse('recipes:article_detail', args=[self.id, self.slug])



class Category(models.Model):
	name = models.CharField(max_length = 30)
	slug = models.SlugField(max_length=200, blank=True)

	def __str__(self):
		return self.name

	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = slugify(self.name)
		super().save(*args, **kwargs)

	def get_absolute_url(self):
		return f"/recipes/articles/{self.slug}/"

class Comment(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='%(class)s_comments_written', on_delete=models.CASCADE)
	body = models.TextField()
	created = models.DateTimeField(auto_now_add=True)

	class Meta:
		abstract=True
		ordering = ('created',)


class RecipeComment(Comment):
	post = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='comments')

class ArticleComment(Comment):
	post = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')





