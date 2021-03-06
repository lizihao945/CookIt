# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from recipes.models import *

from django.contrib.auth.models import User

def getBadges(User):
	badges = []

	# return empty badge set for anonymous user
	if User.is_anonymous:
		return badges

	# First Recipe
	if Content.objects.filter(user=User).count() > 0:
		badges.append(("Chef", "You have your first recipe uploaded!"))

	# First down vote
	for vote in Vote.objects.filter(user=User):
		if not vote.isUp:
			badges.append(("Critic", "Downvote is good!"))
			break;

	# First up vote
	for vote in Vote.objects.filter(user=User):
		if vote.isUp:
			badges.append(("Supporter", "Upvote is good!"))
			break;

	# Number of votes

	# Number of favorites

	return badges
