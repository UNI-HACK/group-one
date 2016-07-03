#encoding:utf-8
from django import forms
from facturacion import models
from datetime import date
from facturacion import models

class ClaveForm(forms.Form):
	oldpassword = forms.CharField(max_length=100, widget=forms.PasswordInput)
	newpassword = forms.CharField(max_length=100, widget=forms.PasswordInput)
	newpassword2 = forms.CharField(max_length=100, widget=forms.PasswordInput)

	def clean_newpassword2(self):
		clean_dictionary = self.cleaned_data
		newpassword2 = clean_dictionary.get('newpassword2')
		newpassword = clean_dictionary.get('newpassword')
		if newpassword != newpassword2:
			raise forms.ValidationError("Las claves no coinciden.")
		if len(newpassword) < 8:
			raise forms.ValidationError("La clave debe tener al menos 8 caracteres.")
		return newpassword2