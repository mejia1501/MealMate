from django import forms
import csv
from django.core.validators import RegexValidator, EmailValidator, MaxValueValidator, MinValueValidator

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



class Datos_Form(forms.Form):
    nombre = forms.CharField(
        max_length=40,
        widget=forms.TextInput(),
        label="Nombre",
        required=True,
        validators=[RegexValidator(regex='^[a-zA-ZáéíóúÁÉÍÓÚñÑ ]+$', message='El nombre solo puede contener letras.')]
    )
    identificacion = forms.CharField(
        max_length=20,
        widget=forms.TextInput(),
        label="Documento de identificación (C.I. o R.I.F)",
        required=True,
        validators=[
        RegexValidator(
            regex=r'^(?:[JGV]{1}[-]?\d{1,9}[-]?\d{1}|[0-9]+)$',
            message='El documento de identificación debe tener un formato válido.'
        )
    ]
    )
    email = forms.EmailField(
        max_length=254,  # Cambiado a 254 para cumplir con el estándar de correos electrónicos
        widget=forms.EmailInput(),
        label="Email",
        required=True,
        validators=[EmailValidator(message='Por favor, ingresa un correo electrónico válido.')]
    )
    telefono = forms.CharField(
        max_length=11,
        min_length=10,
        widget=forms.TextInput(),
        label="Teléfono",
        required=True,
        validators=[RegexValidator(regex='^\d+$', message='El teléfono solo puede contener números.')]
    )

class PagoMovilForm(forms.Form):
    banco = forms.ChoiceField(
        choices=read_banks(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Banca",
        required=True,  
    )
    telefono = forms.CharField(
        label="Teléfono",
        widget=forms.TextInput(attrs={'maxlength': 11, 'minlength': 10}),
        required=True,
        validators=[RegexValidator(regex='^\d+$', message='El teléfono solo puede contener números.')]
    )
    ref = forms.IntegerField(
        label="Número de Referencia",
        widget=forms.TextInput(),
        required=True,
        validators=[MinValueValidator(1, message='La referencia debe ser un número positivo.')]
    )
    nombre = forms.CharField(
        max_length=40,
        widget=forms.TextInput(),
        label="Nombre",
        required=True,
        validators=[RegexValidator(regex='^[a-zA-ZáéíóúÁÉÍÓÚñÑ ]+$', message='El nombre solo puede contener letras.')]
    )

class PagoZelleForm(forms.Form):
    nombre = forms.CharField(
        max_length=40,
        widget=forms.TextInput(),
        label="Nombre del Titular de la Cuenta: ",
        required=True,
        validators=[RegexValidator(regex='^[a-zA-ZáéíóúÁÉÍÓÚñÑ ]+$', message='El nombre solo puede contener letras.')]
    )
    email = forms.EmailField(
        max_length=254,  # Cambiado a 254 para cumplir con el estándar de correos electrónicos
        widget=forms.EmailInput(),
        label="Correo Electrónico Asociado a Zelle",
        required=True,
        validators=[EmailValidator(message='Por favor, ingresa un correo electrónico válido.')]
    )
    telefono = forms.CharField(
        label="Número de Teléfono Asociado a Zelle",
        widget=forms.TextInput(attrs={'maxlength': 11}),
        required=True,
        validators=[RegexValidator(regex='^\d+$', message='El teléfono solo puede contener números.')]
    )
    ref = forms.IntegerField(
        label="Referencia de la transacción",
        widget=forms.TextInput(),
        required=True,
        validators=[MinValueValidator(1, message='La referencia debe ser un número positivo.')]
    )

class PagoPaypalForm(forms.Form):
    ref = forms.IntegerField(
        label="Número de Transacción",
        widget=forms.TextInput(),
        required=True,
        validators=[MinValueValidator(1, message='La referencia debe ser un número positivo.')]
    )
    nombre = forms.CharField(
        max_length=40,
        widget=forms.TextInput(),
        label="Nombre del Titular de la Cuenta",
        required=True,
                validators=[RegexValidator(regex='^[a-zA-ZáéíóúÁÉÍÓÚñÑ ]+$', message='El nombre solo puede contener letras.')]
    )
    email = forms.EmailField(
        max_length=254,  # Cambiado a 254 para cumplir con el estándar de correos electrónicos
        widget=forms.EmailInput(),
        label="<strong>Correo Electrónico Asociado a PayPal</strong><br>",
        required=True,
        validators=[EmailValidator(message='Por favor, ingresa un correo electrónico válido.')]
    )

class EfectivoForm(forms.Form):
    uno=forms.IntegerField(
        min_value=0,
        label="$ 1 ",
        initial=0,
        widget=forms.NumberInput(attrs={'step': '1'})
    )
    cinco=forms.IntegerField(
        min_value=0,
        label="$ 5 ",
        initial=0,
        widget=forms.NumberInput(attrs={'step': '1'})
    )
    diez=forms.IntegerField(
        min_value=0,
        label="$ 10 ",
        initial=0,
        widget=forms.NumberInput(attrs={'step': '1'})
    )
    veinte=forms.IntegerField(
        min_value=0,
        label="$ 20 ",
        initial=0,
        widget=forms.NumberInput(attrs={'step': '1'})
    )
    cincuenta=forms.IntegerField(
        min_value=0,
        label="$ 50 ",
        initial=0,
        widget=forms.NumberInput(attrs={'step': '1'})
    )
    cien=forms.IntegerField(
        min_value=0,
        label="$ 100 ",
        initial=0,
        widget=forms.NumberInput(attrs={'step': '1'})
    )
    