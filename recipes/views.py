# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, reverse, get_object_or_404

# Auth-related
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# Defined models & forms
from recipes.models import *
from recipes.forms import *

def register(request):
	# Registration form
  if request.method == 'GET':
  	context = {'form': RegistrationForm()}
  	return render(request, 'recipes/register.html', context)

	# Registration request
  context = {}
  errors = []
  context['errors'] = errors
  form = RegistrationForm(request.POST)
  if not form.is_valid():
    errors.append(form.errors)
    return render(request, 'recipes/register.html', {'errors': form.errors, 'form': form})
  
  try:
    user = User.objects.create_user(
      username = form.cleaned_data['username'],
      email = form.cleaned_data['email'],
      password = form.cleaned_data['password'])
    user.first_name = form.cleaned_data['first_name']
    user.last_name = form.cleaned_data['last_name']
    user.save()

    return render(request, 'recipes/login.html', context)
  except IntegrityError as e:
    errors.append(e)
    context['form'] = form
    return render(request, 'recipes/register.html', context)

def user_login(request):
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
      login(request, user)
      request.session.set_expiry(0)
      return redirect('home')
    else:
      errors.append('authentication failed')
      return render(request, 'recipes/login.html', context)

def recipe_display(request):
  context = {}
  if request.user.is_authenticated():
    customer = request.user.customer
    context['customer'] = customer
    # for recipe in customer.favorites.all():
      # context['recipe_fav_' + str(recipe.pk)] = True
  context['recipes'] = Recipe.objects.all().order_by('-created_at')
  return render(request, 'recipes/recipe/recipe_display.html', context)

@login_required
def user_logout(request):
  logout(request)
  return redirect('home')

@login_required
def home(request):
  context = {}
  return redirect('recipe_display')
