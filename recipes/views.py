# -*- coding: utf-8 -*-
from __future__ import unicode_literals

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
  for content in context['contents']:
    content.favCount = Favorite.objects.countOfContent(content)
    content.hasFav = Favorite.objects.getFavorite(request.user, content)
    content.voteCount = Vote.objects.countOfContent(content)
  context['badges'] = ['Editor', 'Scholar']
  return render(request, 'recipes/stream.html', context)

@login_required
def myRecipes(request):
  context = {}
  bloguser = Bloguser.objects.get(user=request.user)
  context['bloguser'] = bloguser
  context['page'] = 'myRecipes'
  context['contents'] = list(Content.objects.order_by('-created'))
  return render(request, 'recipes/stream.html', context)

@login_required
def addContent(request):
  if request.method == 'POST':
    context = {}
    errors = []
    context['errors'] = errors
    form = ContentForm(request.POST)
    if form.is_valid():
      try:
        content = Content(user=request.user, text=request.POST['text'])
        content.save()
      except Exception as e:
        errors.append(e)
        context['form'] = form
        return render(request, 'recipes/stream.html', context)
      context['user'] = request.user
      context['contents'] = Content.objects.all()
      return redirect('myRecipes')
    else:
      errors.append(form.errors)
      return render(request, 'recipes/stream.html', context)
  else:
    return redirect('myRecipes')

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
def fav(request):
  contentId = request.POST['content_id']
  content = Content.objects.get(id=contentId)
  fav = Favorite.objects.getFavorite(request.user, content)
  if fav:
    fav.delete()
  else:
    Favorite.objects.create(request.user, content)
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

  return redirect('home')
