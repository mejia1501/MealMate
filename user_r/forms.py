from django import forms
from django.forms import ModelForm
from .models import Restaurante,Ingredientes,Zelle,Paypal,Menu
from django.core.validators import RegexValidator,EmailValidator
import csv
#Lee los bancos registrados en el archivo csv y devuelve una lista con ellos
def read_banks():
    banks = []
    try:
        with open('D:/Uni/lenguaje_programacion_1/proyecto/banks_venezuela.csv', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                banks.append((row[0], row[1]))  # Devuelve tuplas (value, display)
    except FileNotFoundError:
        print("El archivo CSV no se encontró en la ruta especificada.")
    except Exception as e:
        print(f"Ocurrió un error al leer el archivo CSV: {e}")
    return banks

class CuentaRestaurante(ModelForm):
    nombre = forms.CharField(
        widget=forms.TextInput(attrs={
            'maxlength': 40,  # Ajusta según lo que necesites
            'minlength': 1,
            'placeholder': 'Nombre',
        }),
        validators=[RegexValidator(regex='^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s\-\&\']+$', message='El nombre debe tener un formato válido.')]
    )
    
    rif = forms.CharField(
        widget=forms.TextInput(attrs={
            'maxlength': 10,
            'label': 'RIF',
            'placeholder': 'RIF',
        }),
        validators=[RegexValidator(regex='^\d+$', message='El RIF debe tener un formato válido.')]
    )
    
    telefono = forms.CharField(
        widget=forms.TextInput(attrs={
            'maxlength': 11,
            'minlength': 10,
            'placeholder': 'Número de teléfono',
        }),
        validators=[RegexValidator(regex='^\d+$', message='El teléfono solo puede contener números.')]
    )
    
    logo=forms.ImageField(
        label='Suba la el logo de su restaurante',
        widget=forms.ClearableFileInput()
    )

    class Meta:
        model = Restaurante
        fields = ['nombre', 'rif', 'telefono', 'logo']
        
#formulario para actualizar los platos y crearlos
class Items(forms.ModelForm):
    plato = forms.CharField(
        max_length=54,
        label="Plato",
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control','minlength': 1,})
    )
   
    precio = forms.DecimalField(
        min_value=0.00,
        max_value=1000.00,
        max_digits=6,
        decimal_places=2,
        label="Precio",
        required=True,
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        validators=[RegexValidator(regex='^\d+$', message='El numero de telefono solo puede contener números.')]

    )
    #hacer una lista tipo select con css con casillas checkbox y con una barra de busqueda
    ingrediente = Ingredientes.objects.all().order_by('ingrediente')
    OPTIONS = []

    for item in ingrediente:
        OPTIONS.append((item.codigo, item.ingrediente))
        
    ingredientes = forms.MultipleChoiceField(
        widget=forms.SelectMultiple,
        choices=OPTIONS,
        required=True,
        label="Seleccione ingredientes",
    )
    class Meta:
        model=Menu
        fields=['plato','precio','ingredientes']

class PagoForm(forms.Form):
    banco = forms.ChoiceField(
        choices=read_banks(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Banca",
        required=True,  
    )

    efectivo = forms.BooleanField(
        label="¿Trabajara con efectivo?",
        required=False,  # This field is not required by default
    )
    punto_venta = forms.BooleanField(
        label="¿Trabajara con punto de venta?",
        required=False,  # This field is not required by default
    )

    phone = forms.CharField(
        label="Telefono",
        widget=forms.TextInput(attrs={'maxlength': 11,'minlength': 11,}),
        required=True,  # Consider making this field required
        validators=[RegexValidator(regex='^\d+$', message='El numero de telefono solo puede contener números.')]
    )

class PaypalForm(ModelForm):
    nombre = forms.CharField(
        widget=forms.TextInput(attrs={'maxlength': 20}),
        validators=[RegexValidator(regex='^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s\-\&\']+$', message='El nombre debe tener un formato válido.')]
    )
    
    user = forms.CharField(
        widget=forms.TextInput(attrs={'maxlength': 20}),
        validators=[RegexValidator(regex='^[a-zA-Z0-9_.-]+$', message='El usuario solo puede contener letras, números y los caracteres . _ -')]
    )
    
    correo = forms.EmailField(
        widget=forms.EmailInput(attrs={'maxlength': 254}),
        validators=[EmailValidator(message='Por favor, ingresa un correo electrónico válido.')]
    )
    
    phone_p = forms.CharField(
        widget=forms.TextInput(attrs={'maxlength': 11}),
        validators=[RegexValidator(regex='^\d+$', message='El teléfono solo puede contener números.')]
    )

    class Meta:
        model = Paypal
        fields = ['nombre', 'user', 'correo', 'phone_p']
        labels = {
            'nombre': 'Nombre:',
            'user': 'Usuario:',
            'correo': 'Correo:',
            'phone_p': 'Teléfono:',
        }

class ZelleForm(ModelForm):
    mail_z = forms.EmailField(
        widget=forms.EmailInput(attrs={'maxlength': 254}),
        label='Email:',
        validators=[EmailValidator(message='Por favor, ingresa un correo electrónico válido.')]
    )
    
    phone_z = forms.CharField(
        widget=forms.TextInput(attrs={'maxlength': 11, 'minlength': 11}),
        validators=[RegexValidator(regex='^\d+$', message='El teléfono solo puede contener números.')]
    )

    class Meta:
        model = Zelle
        fields = ['mail_z', 'phone_z']
        labels = {
            'mail_z': 'Email:',
            'phone_z': 'Teléfono:',
        }

class AddIngredients(forms.Form):
    ingrediente= forms.CharField(
        max_length=20,
        label="Nombre del ingrediente",
        widget=forms.TextInput()
    )
