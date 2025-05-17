from django import forms
from django.core.validators import RegexValidator

class BarraBusqueda(forms.Form):
    texto = forms.CharField(
        max_length=2750,
        widget=forms.TextInput(attrs={
            'id': 'search',
            'placeholder': 'Buscar...',  
            'autocomplete': 'off', 
        }),
        validators=[
            RegexValidator(regex=r'.+', message='Por favor, ingresa un término de búsqueda.')
        ]
    )


class PedidoForm(forms.Form):
    cantidad = forms.IntegerField(
        required=True,
        label="Cantidad",
        initial=1,
        widget=forms.NumberInput(attrs={'step': '1'}),
        max_value=10,
    )
    nota = forms.CharField(
        label="Nota",
        initial="Vacio.",
        max_length=30,
        widget=forms.Textarea(attrs={
            'placeholder': 'Escribe una nota aquí...'
        }),
        
    )
class UbicacionForm(forms.Form):
    ubicacion=forms.CharField(
        required=True,
        label="Indique la ubicacion del pedido",
        max_length=50,
        widget=forms.TextInput()
    )
