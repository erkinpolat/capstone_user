from django.db import models
from django.conf import settings

# Create your models here.

class Profile(models.Model):
	'''
	Model for the profiles. Stores the user, date_of_birth, photo path, followers and about
	'''

	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	date_of_birth = models.DateField(blank=True, null=True)
	photo = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True)
	followers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='following', blank=True)
	about = models.TextField(blank = True)

	def _str_(self):
		return f'Profile for user {self.user.username}'

	def get_absolute_url(self):
		return f"/account/{self.user.id}/"
