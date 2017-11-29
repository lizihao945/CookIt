from django import forms

from django.contrib.auth.models import User

class RegistrationForm(forms.Form):
	email = forms.EmailField(label='Email',
		widget=forms.EmailInput(attrs=
			{'class': 'form-control', 'placeholder': 'Email'}
		))
	username = forms.CharField(label='Username',
		widget=forms.TextInput(attrs=
			{'class': 'form-control', 'placeholder': 'Username'}
		), required=True)
	first_name = forms.CharField(label='First Name',
		widget=forms.TextInput(attrs=
			{'class': 'form-control', 'placeholder': 'First'}
		))
	last_name = forms.CharField(label='Last Name',
		widget=forms.TextInput(attrs=
			{'class': 'form-control', 'placeholder': 'Last'}
		))
	password = forms.CharField(label='Password', required=True,
		widget=forms.PasswordInput(attrs=
			{'class': 'form-control', 'placeholder': 'Password'}
		))
	password_confirm = forms.CharField(label='Confirm Password', required=True,
		widget=forms.PasswordInput(attrs=
			{'class': 'form-control', 'placeholder': 'Confirm Password'}
		))

	def clean(self):
		cleaned_data = super(RegistrationForm, self).clean()
		password1 = cleaned_data.get('password')
		password2 = cleaned_data.get('password_confirm')
		if password1 and password2 and password1 != password2:
			raise forms.ValidationError("Passwords don't match.")

		return cleaned_data

	def clean_username(self):
		username = self.cleaned_data.get('username')

		if User.objects.filter(username__exact=username):
			raise forms.ValidationError("Username exists.")

		return username
