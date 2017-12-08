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
	url(r'^fav', recipes.views.fav, name='fav'),
	url(r'^voteUp/(?P<contentId>\d+)', recipes.views.voteUp, name='voteUp'),
	url(r'^voteDown/(?P<contentId>\d+)', recipes.views.voteDown, name='voteDown'),
	url(r'^dashboard', recipes.views.dashboard, name='dashboard'),
	url(r'^clearNotifications', recipes.views.clearNotifications, name='clearNotifications'),
]
