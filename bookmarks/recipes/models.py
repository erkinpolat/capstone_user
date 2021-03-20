from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.urls import reverse
from ckeditor.fields import RichTextField
from .functions import resize, merge_images, prepare_cookbook_image
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
from io import BytesIO, StringIO
import sys


# Create your models here.


class CookBook(models.Model):
	'''
	Model for CookBooks. stores user, title, collaborators, picture, template (edited picture inside a notebook), description. slug and time of creation.
	'''
	user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='cookbooks_created', on_delete=models.CASCADE)
	title = models.TextField(max_length=200)
	collaborators = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='cookbooks_collaborating', blank=True)
	picture = models.ImageField(upload_to='cookbook/pictures/%Y/%m/%d/')
	template = models.ImageField(upload_to='cookbook/created/%Y/%m/%d/', blank=True)
	description = models.TextField(blank=True)
	slug = models.SlugField(max_length=200, blank=True)
	created = models.DateField(auto_now_add=True, db_index=True)

	def __str__(self):
		return self.title

	def save(self, *args, **kwargs):
		'''
		function to save the CookBook. uses the function prepare_cookbook_image to create the rendered image for the cookbook
		Saving needs to be handled this way because you cant edit the image fields in Django right away
		'''

		pic = Image.open(self.picture)
		title = str(self.title)
		template = Image.open("./media/cookbook/template/template.png")

		new_template = prepare_cookbook_image(template, pic, title)

		output = BytesIO()

		new_template.save(output, format='PNG')

		output.seek(0)

		self.template = InMemoryUploadedFile(output,'ImageField', "%s.jpg" %self.title, 'image/jpeg', sys.getsizeof(output), None)

		if not self.slug:
			self.slug = slugify(self.title)
		
		super().save(*args, **kwargs)

	def get_absolute_url(self):
		return reverse('recipes:cookbook_detail', args=[self.id, self.slug])

class Recipe(models.Model):
	'''
	Model for a single recipe. Stores user, title, slug, pucture. region. cookbook. country, diet, prep_time, description,
	steps, ingredients, time of created and users that liked the recipe
	'''
	user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='recipes_created', on_delete=models.CASCADE)
	title = models.CharField(max_length = 200)
	slug = models.SlugField(max_length=200, blank=True)
	picture = models.ImageField(upload_to='recipes/%Y/%m/%d/', blank=True)
	region = models.ForeignKey('Region', related_name='recipes_from_region', on_delete=models.SET('None'))
	cookbook = models.ForeignKey('CookBook', related_name='recipes_in_cookbook', on_delete=models.CASCADE)
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
		'''
		Upon saving a slug is created
		'''
		if not self.slug:
			self.slug = slugify(self.title)
		super().save(*args, **kwargs)

	def get_absolute_url(self):
		return reverse('recipes:detail', args=[self.id, self.slug])



class Diet(models.Model):
	'''
	Model for dietary prefeerences. The recipe model uses the instances here as categories to choose from.
	'''
	name = models.CharField(max_length = 30)
	slug = models.SlugField(max_length=200, blank=True)


	def __str__(self):
		return self.name

	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = slugify(self.name)
		super().save(*args, **kwargs)

class Region(models.Model):
	'''
	Model for different regions. The recipe model uses the instances here as categories to choose from.
	'''
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
	'''
	Model for articles. Stores user, title, slug, category, picture, description, time of creation and users that liked the article.
	'''
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
		'''
		A slug is created upon saving
		'''
		if not self.slug:
			self.slug = slugify(self.title)
		super().save(*args, **kwargs)

	def get_absolute_url(self):
		return reverse('recipes:article_detail', args=[self.id, self.slug])



class Category(models.Model):
	'''
	Model for different article categories. The recipe model uses the instances here as categories to choose from.
	'''
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
	'''
	Model for comments. Stores user associated, the content of the comment and the time of creation. Is a superclass.
	'''
	user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='%(class)s_comments_written', on_delete=models.CASCADE)
	body = models.TextField()
	created = models.DateTimeField(auto_now_add=True)

	class Meta:
		abstract=True
		ordering = ('created',)


class RecipeComment(Comment):
	'''
	Recipe comment model that inherits from the Comment model. Stores the recipe associated with as well.
	'''
	post = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='comments')

class ArticleComment(Comment):
	'''
	Article comment model that inherits from the Comment model. Stores the article associated with as well.
	'''
	post = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')





