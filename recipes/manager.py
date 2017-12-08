from django.db import models
from django.core.exceptions import ObjectDoesNotExist

class FavoriteManager(models.Manager):
  def forUser(self, user):
    return self.get_queryset().filter(user=user)

  def countOfContent(self, content):
    return self.get_queryset().filter(content=content).count()

  def getFavorite(self, user, content):
    try:
      return self.get_queryset().get(user=user, content=content)
    except ObjectDoesNotExist:
      return None

  def create(self, user, content):
    return super(FavoriteManager, self).create(user=user, content=content)

class VoteManager(models.Manager):
  def forUser(self, user):
    return self.get_queryset().filter(user=user)

  def countOfContent(self, content):
    rt = 0
    for v in self.get_queryset().filter(content=content):
      if v.isUp == True:
        rt += 1
      else:
        rt -= 1
    return rt

  def getVote(self, user, content):
    try:
      return self.get_queryset().get(user=user, content=content)
    except ObjectDoesNotExist:
      return None

  def create(self, user, content, isUp):
    return super(VoteManager, self).create(user=user, content=content, isUp=isUp)
