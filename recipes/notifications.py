# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from recipes.models import *

from django.contrib.auth.models import User


def getNotification(user):
    if user.is_anonymous:
        return []
    else:
        Notification.objects.filter(user=user).order_by('-created')


def clearNotifications(user):
    Notification.objects.filter(user=user).delete()