# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect, reverse, get_object_or_404

# Auth-related
from django.contrib import auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator

# DB-related
from django.db import IntegrityError
from django.db import transaction

# Defined models & forms
from recipes.models import *
from recipes.forms import *

from recipes.badges import *
from recipes.notifications import *

# for searching
import re

stopwords = set(["i", "want", "eat", "lunch", "dinner", "breakfast", "how", "what", "why", "cook", "make", "a", "an", "and", "are", "as", "at", "be", "by", "for", "from", "has", "he", "in", "is", "it", "its", "of", "on", "that", "the", "to", "was", "were", "will", "with"])

@transaction.atomic
def register(request):
  if request.method == 'POST':
    context = {}
    errors = []
    context['errors'] = errors
    form = RegistrationForm(request.POST)
    if form.is_valid():
      try:
        user = User.objects.create_user(
          username = form.cleaned_data['username'],
          email = form.cleaned_data['email'],
          password = form.cleaned_data['password'])
        user.first_name = form.cleaned_data['firstName']
        user.last_name = form.cleaned_data['lastName']
        user.save()

        auth.login(request, user)

        bloguser = Bloguser(user=user)
        bloguser.save()

        return redirect('home')
      except IntegrityError as e:
        errors.append(e)
        context['form'] = form
        return render(request, 'recipes/register.html', context)
    else:
      errors.append(form.errors)
      return render(request, 'recipes/register.html', {'errors': form.errors, 'form': form})
  else:
    context = {'form': RegistrationForm()}
    return render(request, 'recipes/register.html', context)

def login(request):
  context = {}
  errors = []
  context['errors'] = errors
  if request.method == 'GET':
    return render(request, 'recipes/login.html', context)
  else:
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
      auth.login(request, user)
      return redirect('home')
    else:
      errors.append('authentication failed')
      return render(request, 'recipes/login.html', context)

def logout(request):
  auth.logout(request)
  return redirect('/')

def home(request):
  context = {}
  if not request.user.is_anonymous:
    bloguser = Bloguser.objects.get(user=request.user)
    context['bloguser'] = bloguser
  context['page'] = 'home'
  context['contents'] = list(Content.objects.order_by('-created'))

  def get_bag(doc_str):
    bag = [w.lower() for w in re.findall('\\w+', doc_str)]
    bag = list(filter(lambda x: x not in stopwords, bag))
    return set(bag)

  recommend_for_user = set()

  for content in context['contents']:
    user_in_favor = False
    content.favCount = Favorite.objects.countOfContent(content)
    content.hasFav = Favorite.objects.getFavorite(request.user, content)
    if content.hasFav is not None:
      user_in_favor = True
    content.voteCount = Vote.objects.countOfContent(content)

    recommendation_set = []
    this_bag = get_bag(content.text)
    for target_content in context['contents']:
        if (target_content != content):
            target_bag = get_bag(target_content.text)
            relation = float(len(list(filter(lambda x: x in target_bag, list(this_bag))))) / float(len(this_bag))
            if (relation > 0.4):
                recommendation_set.append(target_content)
    content.recommendations = recommendation_set

    t = Vote.objects.getVote(request.user, content)
    if t == None:
      content.hasVote = 0
    elif t.isUp == True:
      content.hasVote = 1
      user_in_favor = True
    else:
      content.hasVote = -1

    if user_in_favor:
      recommend_for_user.update(recommendation_set)


  context['badges'] = getBadges(request.user)
  context['notifications'] = getNotification(request.user)
  context['suggestions'] = list(recommend_for_user)

  return render(request, 'recipes/stream.html', context)

@login_required
def addContent(request):
  if request.method == 'POST':
    context = {}
    errors = []
    context['errors'] = errors
    content = Content(user=request.user)
    content.text = "<h5>Ingredients:</h5>" + request.POST['ingredients'] + "<br><br><h5>Steps:</h5>" + request.POST['text']

    form = ContentForm(request.POST, request.FILES, instance=content)
    if form.is_valid():
      form.save()
    else:
      print(form.errors)

    context['user'] = request.user
    context['contents'] = Content.objects.all()
    return redirect('home')
  else:
    return redirect('home')

@login_required
def deleteContent(request, contentId):
  context = {}
  try:
    content_to_delete = Content.objects.get(id=contentId)
    content_to_delete.delete()
  except ObjectDoesNotExist as e:
    pass

  context['contents'] = Content.objects.all()
  return redirect('home')

@login_required
def notifications(request, contentId):
  return ''

@login_required
@transaction.atomic
def fav(request):
  contentId = request.POST['content_id']
  content = Content.objects.get(id=contentId)
  fav = Favorite.objects.getFavorite(request.user, content)
  if fav:
    fav.delete()
    notification = Notification(user=content.user, text="Your content is unfavorited!")
    notification.save()
  else:
    Favorite.objects.create(request.user, content)
    notification = Notification(user=content.user, text="Your content is favorited!")
    notification.save()

  return redirect('home')

@login_required
def voteUp(request, contentId):
  content = Content.objects.get(id=contentId)
  vote = Vote.objects.getVote(request.user, content)

  if vote:
    if not vote.isUp:
      vote.delete()
    else:
      return redirect('home')
  else:
    Vote.objects.create(request.user, content, True)

  notification = Notification(user=content.user, text="Your content is up-voted!")
  notification.save()
  return redirect('home')

@login_required
def voteDown(request, contentId):
  content = Content.objects.get(id=contentId)
  vote = Vote.objects.getVote(request.user, content)

  if vote:
    if vote.isUp:
      vote.delete()
    else:
      return redirect('home')
  else:
    Vote.objects.create(request.user, content, False)

  notification = Notification(user=content.user, text="Your content is down-voted!")
  notification.save()
  return redirect('home')

@login_required
def dashboard(request):
  context = {}
  context['contents'] = list(Content.objects.filter(user=request.user).order_by('-created'))
  for content in context['contents']:
    content.favCount = Favorite.objects.countOfContent(content)
    content.hasFav = Favorite.objects.getFavorite(request.user, content)
    content.voteCount = Vote.objects.countOfContent(content)

  context['badges'] = getBadges(request.user)
  context['notifications'] = getNotification(request.user)

  context['favCount'] = Favorite.objects.countOfUser(request.user)
  context['voteCount'] = Vote.objects.countOfUser(request.user)

  return render(request, 'recipes/dashboard.html', context)


def search(request):
  if request.method == 'POST':
    original_query = request.POST['searchQuery'].lower()
  else:
    original_query = request.GET['searchQuery'].lower()
  original_tokens = re.findall("\w+", original_query)

  # drop stop words
  original_tokens = list(filter(lambda w : w not in stopwords, original_tokens))

  # Empty query, return to home
  if len(original_tokens) is 0:
    return redirect('home')

  context = {}
  if not request.user.is_anonymous:
    bloguser = Bloguser.objects.get(user=request.user)
    context['bloguser'] = bloguser
  context['page'] = 'home'
  unfiltered = list(Content.objects.order_by('-created'))
  all_matched = []
  partial_matched = []
  for content in unfiltered:
    searchRange = ' '.join([content.user.username, content.title, content.text] + [w.text for w in content.tag_set.all()])
    docTokens = set([w.lower() for w in re.findall('\\w+', searchRange)])
    all_match = True
    partial_match = False
    for query_token in original_tokens:
      all_match = all_match and (query_token in docTokens)
      partial_match = partial_match or (query_token in docTokens)
    if all_match:
      all_matched.append(content)
    if partial_match:
      partial_matched.append(content)

  if len(all_matched) is not 0:
    context['contents'] = all_matched
    context['query'] = ' AND '.join(original_tokens)
    context['resultCount'] = len(all_matched)
  else:
    context['contents'] = partial_matched
    context['query'] = ' OR '.join(original_tokens)
    context['resultCount'] = len(partial_matched)

  for content in context['contents']:
    content.favCount = Favorite.objects.countOfContent(content)
    content.hasFav = Favorite.objects.getFavorite(request.user, content)
    content.voteCount = Vote.objects.countOfContent(content)
    t = Vote.objects.getVote(request.user, content)
    if t == None:
      content.hasVote = 0
    elif t.isUp == True:
      content.hasVote = 1
    else:
      content.hasVote = -1

  context['badges'] = getBadges(request.user)
  context['notifications'] = getNotification(request.user)

  return render(request, 'recipes/search_results.html', context)

@login_required
def addTag(request):
  contentId = request.POST['contentId']
  tag = request.POST['tag']

  content = Content.objects.get(id=contentId)

  if Tag.objects.filter(text=tag):
    tagObj = Tag.objects.get(text=tag)
    tagObj.contents.add(content)
    tagObj.save()
  else:
    tagObj = Tag(text=tag)
    tagObj.save()
    tagObj.contents.add(content)
    tagObj.save()

  return redirect('home')

@login_required
def clearNotifications(request):
  clearAllNotifications(request.user)
  return redirect('home')
