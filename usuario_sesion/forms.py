from django import forms
from django.forms import ModelForm
from user_r.models import Restaurante,Cliente
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator,EmailValidator


class CreateNewRestauranteForm(UserCreationForm):
     
    nombre=forms.CharField(
         widget=forms.TextInput(attrs={
             'maxlength': 20,
             'placeholder':'Nombre',
             
             } )
     )
    email=forms.EmailField(widget=forms.EmailInput(attrs={
        'maxlength': 100,
        'placeholder':'Email',
        
        }),
        validators=[EmailValidator(message='Por favor, ingresa un correo electrónico válido.')])
    rif=forms.CharField(widget=forms.TextInput(attrs={
        'maxlength': 20,
        'label': 'RIF',
        'placeholder':'RIF',
        
        }),
        validators=[RegexValidator(regex='^\d+$', message='La RIF solo puede contener números.')]
        )
        
    telefono=forms.CharField(widget=forms.TextInput(attrs={
        'maxlength': 11,
        'minlength': 10,
        'placeholder':'Numero de telefono',
        
        }),
        validators=[RegexValidator(regex='^\d+$', message='La RIF solo puede contener números.')]
        )
    class Meta:
        model = Restaurante
        fields = ['nombre','username' ,'rif','email','telefono','password1','password2',]
        
   
class IniciarSesion(forms.Form):
    email = forms.EmailField(
        max_length=254,
        required=True,
        widget=forms.TextInput(attrs={ 
         'placeholder': 'Ingresa tu mail', 'class': 'form-control' }),
        validators=[EmailValidator(message='Por favor, ingresa un correo electrónico válido.')]
        )
    password = forms.CharField(
        max_length=18,
        widget=forms.PasswordInput(attrs={ 'placeholder': 'Ingresa tu contraseña','minlength': 1,'class': 'form-control'
    }))


class CreateNewClientForm(UserCreationForm):
    nombre=forms.CharField(
         widget=forms.TextInput(attrs={
             'placeholder':'Nombre',
             'maxlength': 40,
             } ),
        validators=[RegexValidator(regex='^[a-zA-ZáéíóúÁÉÍÓÚñÑ ]+$', message='El nombre solo puede contener letras.')]
     )
    email=forms.EmailField(
        widget=forms.EmailInput(attrs={
        'maxlength': 100,
        'placeholder':'Email',
        }),
        validators=[EmailValidator(message='Por favor, ingresa un correo electrónico válido.')]
        )
    cedula=forms.CharField(widget=forms.TextInput(attrs={
        'maxlength': 8,
        'minlength': 1,
        'label': 'Cedula',
        }),
        validators=[RegexValidator(regex='^\d+$', message='La cédula solo puede contener números.')]
        )
    telefono=forms.CharField(widget=forms.TextInput(attrs={
        'maxlength': 11,
        'minlength': 10,
        'placeholder':'Numero de telefono',
        
        }),
        validators=[RegexValidator(regex='^\d+$', message='El numero de telefono solo puede contener números.')]
        )
  
    model=Cliente
    fields = ['nombre','telefono', 'cedula','email', 'username', 'password1','password2'] 

class CuentaCliente(ModelForm):
    nombre=forms.CharField(
         widget=forms.TextInput(attrs={
             'placeholder':'Nombre',
             'maxlength': 40,
             } ),
        validators=[RegexValidator(regex='^[a-zA-ZáéíóúÁÉÍÓÚñÑ ]+$', message='El nombre solo puede contener letras.')]
     )
    telefono=forms.CharField(widget=forms.TextInput(attrs={
        'maxlength': 11,
        'minlength': 10,
        'placeholder':'Numero de telefono',
        
        }),
        validators=[RegexValidator(regex='^\d+$', message='El numero de telefono solo puede contener números.')]
        )
    class Meta:
        model=Cliente
        fields=['nombre','telefono']
