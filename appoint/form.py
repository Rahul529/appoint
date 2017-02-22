from .models import StaffNew
from django import forms
from django.contrib.auth.forms import AuthenticationForm

class StaffForm(forms.Form):
	username = forms.CharField(label='username',widget=forms.TextInput(attrs={'class':'form-control','name':'username'}))
	password= forms.CharField(label='Password',widget=forms.PasswordInput(attrs={'class':'form-control','name':'password'}))

	# class Meta:
	# 	model = StaffNew
	# 	fields = ['username','password']