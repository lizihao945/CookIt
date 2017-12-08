from django import template
from django.template.loader import render_to_string

from recipes.models import Favorite

register = template.Library()

@register.simple_tag(takes_context=True)
def fav_tag(context, content):
  user = context['request'].user
  if not user.is_authenticated():
    context = {}
    context['contentId'] = content.pk
    context['undo'] = False
    context['fav_count'] = Favorite.objects.for_content(content).count()
    return render_to_string('fav/fav_block.html', context)

  if Favorite.objects.get_favorite(user, content):
    undo = True
  else:
    undo = False

  context = {}
  context['contentId'] = content.pk
  context['undo'] = undo
  context['fav_count'] = Favorite.objects.for_content(content).count()
  return render_to_string('fav/fav_block.html', context)
