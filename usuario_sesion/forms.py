from django import forms
from django.forms import ModelForm
from .models import Cliente
from user_r.models import Restaurante
from django.contrib.auth.forms import UserCreationForm

class CreateNewRestaurante(UserCreationForm):
     class Meta:
        model = Restaurante
        fields = ['nombre', 'rif','telefono','username','email','password1','password2']
        widgets = { 
                'fundacion': forms.DateInput(attrs={'type': 'date'}),
                'telefono': forms.TextInput(attrs={'maxlength': 11}),
                'nombre': forms.TextInput(attrs={'maxlength': 20}),
                'rif': forms.TextInput(attrs={'maxlength': 20,'label': 'RIF',}),
                'email': forms.EmailInput(attrs={'maxlength': 254}),
            }
   
class IniciarSesion(forms.Form):
    email = forms.EmailField(label='Email',max_length=254,required=True,widget=forms.TextInput(attrs={ 
        'class': 'form-group', 'placeholder': 'Ingresa tu mail' }))
    password = forms.CharField(label='Contraseña',max_length=18,widget=forms.PasswordInput(attrs={'class': 'form-group', 'placeholder': 'Ingresa tu contraseña'
    }))

class CreateNewCliente(UserCreationForm):
    class Meta:
        model=Cliente
        fields = ['nombre','telefono', 'cedula','username','email','password1','password2']   
        widgets = { 
                'telefono': forms.TextInput(attrs={'maxlength': 11}),
                'nombre': forms.TextInput(attrs={'maxlength': 20}),
                'cedula': forms.TextInput(attrs={'maxlength': 8}),
                'email': forms.EmailInput(attrs={'maxlength': 254}),
            }

class CuentaCliente(ModelForm):
    class Meta:
        model=Cliente
        fields=['nombre','telefono']
