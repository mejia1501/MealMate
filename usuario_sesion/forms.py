from django import forms
from django.forms import ModelForm
from .models import Cliente

class CreateNewRestaurante(forms.Form):
    
    nombre = forms.CharField(label='Nombre',max_length=20)
    password1 = forms.CharField(label='Contraseña',max_length=18)
    password2 = forms.CharField(label='Repita la contraseña',max_length=18)
    rif = forms.CharField(label="RIF",max_length=20)
    email = forms.EmailField(label='Email',max_length=254)
    telefono = forms.CharField(label='Telefono',max_length=11)
    direccion = forms.CharField(label='Direccion',max_length=200)
    fundacion = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    logo=forms.CharField(max_length=100)

class IniciarSesion(forms.Form):
    email = forms.EmailField(label='Email',max_length=254,widget=forms.TextInput(attrs={ 
        'class': 'form-group', 'placeholder': 'Ingresa tu mail' }))
    password = forms.CharField(label='Contraseña',max_length=18,widget=forms.PasswordInput(attrs={'class': 'form-group', 'placeholder': 'Ingresa tu contraseña'
    }))

class CreateNewCliente(forms.Form):
    
    nombre = forms.CharField(label='Nombre',max_length=20)
    password1 = forms.CharField(label='Contraseña',max_length=18)
    password2 = forms.CharField(label='Repita la contraseña',max_length=18)
    cedula = forms.CharField(label="Cedula",max_length=8)
    email = forms.EmailField(label='Email',max_length=254)
    telefono = forms.CharField(label='Telefono',max_length=11)

class CuentaCliente(ModelForm):
    class Meta:
        model=Cliente
        fields=['nombre','telefono']
