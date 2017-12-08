from django.conf.urls import url
from django.conf import settings

import recipes.views

urlpatterns = [
	url(r'^$', recipes.views.home, name='home'),
	url(r'^login', recipes.views.login, name='login'),
	url(r'^logout', recipes.views.logout, name='logout'),
	url(r'^register', recipes.views.register, name='register'),
	url(r'^myRecipes', recipes.views.myRecipes, name='myRecipes'),
	url(r'^addContent', recipes.views.addContent, name='addContent'),
	url(r'^notifications', recipes.views.notifications, name='notifications'),
]
