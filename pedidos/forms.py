from django import forms
from django.forms import ModelForm
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

class Datos_Form(forms.Form):
    nombre=forms.CharField(
        max_length=40,
        widget=forms.TextInput(),
        label="<strong>Nombre</strong><br>",
        required=True,

    )
    identificacion=forms.CharField(
        max_length=20,
        widget=forms.TextInput(),
        label="<strong>Documento de identificacion (C.I. o R.I.F)</strong><br>",
        required=True,
    )
    email=forms.EmailField(
        max_length=20,
        widget=forms.EmailInput(),
        label="<strong>Email</strong><br>",
        required=True,
    )
    telefono=forms.CharField(
        max_length=11,
        widget=forms.TextInput(),
        label="<strong>Teléfono</strong><br>",
        required=True,
    )

class PagoMovilForm(forms.Form):
    banco = forms.ChoiceField(
        choices=read_banks(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Banca",
        required=True,  
    )
    telefono = forms.CharField(
        label="Telefono",
        widget=forms.TextInput(attrs={'maxlength': 11}),
        required=True,
    )
    ref=forms.IntegerField(
        label="Número de Referencia",
        widget=forms.TextInput,
        required=True,   
    )
    nombre=forms.CharField(
        max_length=40,
        widget=forms.TextInput(),
        label="Nombre",
        required=True,
    )
    hora=forms.TimeField(
        widget=forms.TimeInput(),
        required=True,
        label="Hora del pago",
    )

class PagoZelleForm(forms.Form):
    ref=forms.IntegerField(
        label="Número de Referencia de la Transacción",
        widget=forms.TextInput,
        required=True,   
    )
    hora=forms.TimeField(
        widget=forms.TimeInput(),
        required=True,
        label="<strong>Hora del pago</strong><br>",
    )
    nombre=forms.CharField(
        max_length=40,
        widget=forms.TextInput(),
        label="<strong>Nombre del Titular de la Cuenta:</strong><br>",
        required=True,
    )
    email=forms.EmailField(
        max_length=20,
        widget=forms.EmailInput(),
        label="<strong>Correo Electrónico Asociado a Zelle</strong><br>",
        required=True,
    )
    telefono = forms.CharField(
        label="Número de Teléfono Asociado a Zelle",
        widget=forms.TextInput(attrs={'maxlength': 11}),
        required=True,
    )

class PagoPaypalForm(forms.Form):
    ref=forms.IntegerField(
        label="Número de Transacción ",
        widget=forms.TextInput,
        required=True,   
    )
    hora=forms.TimeField(
        widget=forms.TimeInput(),
        required=True,
        label="<strong>Hora del pago</strong><br>",
    )
    nombre=forms.CharField(
        max_length=40,
        widget=forms.TextInput(),
        label="<strong>Nombre del Titular de la Cuenta:</strong><br>",
        required=True,
    )
    email=forms.EmailField(
        max_length=20,
        widget=forms.EmailInput(),
        label="<strong>Correo Electrónico Asociado a PayPal</strong><br>",
        required=True,
    )
