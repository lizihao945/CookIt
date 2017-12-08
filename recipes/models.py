# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User

from recipes.manager import FavoriteManager

class Bloguser(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	picture = models.ImageField(upload_to='cookit-headshots', blank=True)

	def __str__(self):
		return str(self.user)

class Content(models.Model):
	user = models.ForeignKey(User, blank=False, null=False)
	text = models.CharField(max_length=1000)
	created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return str(self.user) + ': ' + str(self.text)

class Favorite(models.Model):
	user = models.ForeignKey(User, blank=False, null=False, related_name='favorites')
	content = models.ForeignKey(Content, blank=False, null=False, related_name='favorites')

	objects = FavoriteManager()
