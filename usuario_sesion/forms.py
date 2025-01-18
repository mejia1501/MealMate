from django import forms
from django.forms import ModelForm
from .models import Cliente
from user_r.models import Restaurante
from django.contrib.auth.forms import UserCreationForm

class CreateNewRestauranteForm(UserCreationForm):
     
    nombre=forms.CharField(
         widget=forms.TextInput(attrs={
             'maxlength': 11,
             'minlength': 10,
             'placeholder':'Nombre',
             
             } )
     )
    username=forms.CharField(
         widget=forms.TextInput(attrs={
             'maxlength': 18,
             'label':'Usuario',
             } )
     )
    email=forms.EmailField(widget=forms.EmailInput(attrs={
        'maxlength': 254,
        'placeholder':'Email',
        
        }))
    rif=forms.CharField(widget=forms.TextInput(attrs={
        'maxlength': 10,
        'label': 'RIF',
        'placeholder':'RIF',
        
        }))
    telefono=forms.CharField(widget=forms.TextInput(attrs={
        'maxlength': 11,
        'minlength': 10,
        'placeholder':'Numero de telefono',
        
        }),)
    password1=forms.CharField(widget=forms.PasswordInput(attrs={
        'maxlength':18,
        'placeholder':'Contraseña',
        
        }))
    password2=forms.CharField(widget=forms.PasswordInput(attrs={
        'maxlength':18,
        'placeholder':'Confirme la Contraseña',
        
        }))
    class Meta:
        model = Restaurante
        fields = ['nombre','username' ,'rif','email','telefono','password1','password2']
        
   
class IniciarSesion(forms.Form):
    email = forms.EmailField(label='Email',max_length=254,required=True,widget=forms.TextInput(attrs={ 
        'class': 'form-group', 'placeholder': 'Ingresa tu mail' }))
    password = forms.CharField(label='Contraseña',max_length=18,widget=forms.PasswordInput(attrs={'class': 'form-group', 'placeholder': 'Ingresa tu contraseña','minlength': 1,
    }))


class CreateNewClientForm(UserCreationForm):
     
    nombre=forms.CharField(
         widget=forms.TextInput(attrs={
             'maxlength': 11,
             'minlength': 10,
             'placeholder':'Nombre',
             
             } )
     )
    email=forms.EmailField(widget=forms.EmailInput(attrs={
        'maxlength': 254,
        'placeholder':'Email',
        
        }))
    cedula=forms.CharField(widget=forms.TextInput(attrs={
        'maxlength': 11,
        'minlength': 10,
        'label': 'RIF',
        'placeholder':'RIF',
        
        }))
    telefono=forms.CharField(widget=forms.TextInput(attrs={
        'maxlength': 11,
        'minlength': 10,
        'placeholder':'Numero de telefono',
        
        }),)
    password1=forms.CharField(widget=forms.PasswordInput(attrs={
        'maxlength':18,
        'placeholder':'Contraseña',
        
        }))
    password2=forms.CharField(widget=forms.PasswordInput(attrs={
        'maxlength':18,
        'placeholder':'Confirme la Contraseña',
        
        }))
  
    model=Cliente
    fields = ['nombre','telefono', 'cedula','email',] 

class CuentaCliente(ModelForm):
    class Meta:
        model=Cliente
        fields=['nombre','telefono']
