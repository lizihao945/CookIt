from django.conf.urls import url
from django.conf import settings

import recipes.views

urlpatterns = [
	url(r'^$', recipes.views.home, name='home'),
	url(r'^login', recipes.views.user_login, name='login'),
	url(r'^logout', recipes.views.user_logout, name='logout'),
	url(r'^register', recipes.views.register, name='register'),
]
