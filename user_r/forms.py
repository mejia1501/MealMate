from django import forms
from django.forms import ModelForm
from .models import Restaurante,Ingredientes,Pago,Zelle,Paypal,Menu
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
     class Meta:
        model = Restaurante
        fields = ['nombre', 'telefono', 'direccion', 'fundacion', 'logo']
        widgets = { 
            'fundacion': forms.DateInput(attrs={'type': 'date'}),
            'telefono': forms.TextInput(attrs={'maxlength': 11}),
            'nombre': forms.TextInput(attrs={'maxlength': 20}),
            'logo': forms.TextInput(attrs={'maxlength': 100}),
        }
#formulario para actualizar los platos y crearlos
class Items(forms.ModelForm):
    plato = forms.CharField(
        max_length=54,
        label="Plato",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    precio = forms.DecimalField(
        min_value=0.00,
        max_value=1000.00,
        max_digits=6,
        decimal_places=2,
        label="Precio",
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    #hacer una lista tipo select con css con casillas checkbox y con una barra de busqueda
    ingredientes = forms.ModelMultipleChoiceField(
        queryset=Ingredientes.objects.all(),
        label="Seleccione ingredientes",
        to_field_name='codigo'
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

    phone = forms.CharField(
        label="Telefono",
        widget=forms.TextInput(attrs={'maxlength': 11}),
        required=True,  # Consider making this field required
    )

class PaypalForm(ModelForm):
    class Meta:
        model = Paypal
        fields = ['nombre', 'user', 'correo', 'phone_p']
        widgets = {
            'nombre': forms.TextInput(attrs={'maxlength': 20}),
            'user': forms.TextInput(attrs={'maxlength': 20}),
            'correo': forms.EmailInput(attrs={'maxlength': 254}),
            'phone_p': forms.TextInput(attrs={'maxlength': 11}),
        }
        labels = {
            'nombre': 'Nombre:',
            'user': 'Usuario:',
            'correo': 'Correo:',
            'phone_p': 'Teléfono:',
        }

class ZelleForm(ModelForm):
    class Meta:
        model = Zelle
        fields = ['mail_z', 'phone_z']
        widgets = {
            'mail_z': forms.EmailInput(attrs={'maxlength': 254}),
            'phone_z': forms.TextInput(attrs={'maxlength': 11}),
        }
        labels = {
            'mail_z': 'Email:',
            'phone_z': 'Telefono:',
        }

class AddIngredients(forms.Form):
    ingrediente= forms.CharField(
        max_length=20,
        label="Nombre del ingrediente",
        widget=forms.TextInput()
    )
