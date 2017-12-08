from django.db import models
from django.core.exceptions import ObjectDoesNotExist

class FavoriteManager(models.Manager):
  def for_user(self, user):
    return self.get_queryset().filter(user=user)

  def for_content(self, content):
    return self.get_queryset().filter(content=content)

  def get_favorite(self, user, content):
    try:
      return self.get_queryset().get(user=user, content=content)
    except ObjectDoesNotExist:
      return None

  def create(self, user, content):
    return super(FavoriteManager, self).create(user=user, content=content)
