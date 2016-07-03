#encoding:utf-8
from django import forms
from facturacion import models
from datetime import date

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


class ProductoForm(forms.ModelForm):	
	class Meta:
		model = models.Producto
		fields = "__all__"

	def clean_cantidad(self):
		clean_dictionary = self.cleaned_data
		cantidad = clean_dictionary.get('cantidad')
		if cantidad < 0:
			raise forms.ValidationError("El valor debe ser mayor o igual a cero.")
		return cantidad

	def clean_en_descomposicion(self):
		clean_dictionary = self.cleaned_data
		en_descomposicion = clean_dictionary.get('en_descomposicion')
		if en_descomposicion < 0:
			raise forms.ValidationError("El valor debe ser mayor o igual a cero.")
		return en_descomposicion

	def __init__(self, *args, **kwargs):
		super(ProductoForm, self).__init__(*args, **kwargs)
		self.fields['vendedor'].widget.attrs['disabled'] = True
#labs = Laboratory.objects.filter(enable=True)
#self.fields['laboratory'].queryset = labs

class FacturaForm(forms.ModelForm):	
	class Meta:
		model = models.Factura
		fields = "__all__"