# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from recipes.models import *

from django.contrib.auth.models import User


def getNotification(user):
    if user.is_anonymous:
        return []
    else:
        return Notification.objects.filter(user=user).order_by('-created')



def clearAllNotifications(user):
    Notification.objects.filter(user=user).delete()