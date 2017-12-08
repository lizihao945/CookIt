# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms

from django.contrib.auth.models import User

from recipes.models import *

from django.utils.translation import ugettext_lazy as _

class RegistrationForm(forms.Form):

	email = forms.EmailField(label='Email',
		widget=forms.EmailInput(attrs=
			{'class': 'form-control', 'placeholder': 'Email'}
		))
	username = forms.CharField(label='Username',
		widget=forms.TextInput(attrs=
			{'class': 'form-control', 'placeholder': 'Username'}
		), required=True)
	firstName = forms.CharField(label='First Name',
		widget=forms.TextInput(attrs=
			{'class': 'form-control', 'placeholder': 'First'}
		))
	lastName = forms.CharField(label='Last Name',
		widget=forms.TextInput(attrs=
			{'class': 'form-control', 'placeholder': 'Last'}
		))
	password = forms.CharField(label='Password', required=True,
		widget=forms.PasswordInput(attrs=
			{'class': 'form-control', 'placeholder': 'Password'}
		))
	passwordConfirm = forms.CharField(label='Confirm Password', required=True,
		widget=forms.PasswordInput(attrs=
			{'class': 'form-control', 'placeholder': 'Confirm Password'}
		))


	def clean(self):
		cleaned_data = super(RegistrationForm, self).clean()
		password1 = cleaned_data.get('password')
		password2 = cleaned_data.get('passwordConfirm')
		if password1 and password2 and password1 != password2:
			raise forms.ValidationError("Passwords did not match.")

		return cleaned_data

	def clean_username(self):
		username = self.cleaned_data.get('username')

		if User.objects.filter(username__exact=username):
			raise forms.ValidationError("Username is already taken.")

		return username

class UserForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ['first_name', 'last_name']
		widgets = {
			'first_name': forms.TextInput(attrs=
				{'class': 'form-control', 'placeholder': 'First'}
			),

			'last_name': forms.TextInput(attrs=
					{'class': 'form-control', 'placeholder': 'Last'}
			),
		}
		labels = {
			'first_name': _('First Name'),
			'last_name': _('Last Name'),
		}

	password = forms.CharField(label='Password', required=False,
	widget=forms.PasswordInput(attrs=
		{'class': 'form-control', 'placeholder': 'Password'}
	))
	passwordConfirm = forms.CharField(label='Confirm Password', required=False,
	widget=forms.PasswordInput(attrs=
		{'class': 'form-control', 'placeholder': 'Confirm Password'}
	))

class BloguserForm(forms.ModelForm):
	class Meta:
		model = Bloguser
		exclude = ('user',)
		widgets = {
			'age': forms.NumberInput(attrs=
					{'class': 'form-control', 'placeholder': 'Enter your age'}
			),
			'bio': forms.Textarea(attrs=
					{'class': 'form-control', 'placeholder': 'You can type a short bio here (within 420 characters)'}
			),
			'picture': forms.FileInput(),
		}

		labels = {
			'age': _('Enter your age'),
			'bio': _('Short Bio'),
		}

class ContentForm(forms.Form):
	text = forms.CharField(max_length=42)
