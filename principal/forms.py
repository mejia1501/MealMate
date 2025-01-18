from django import forms
class BarraBusqueda(forms.Form):
    texto = forms.CharField(
        label="Buscar",
        max_length=2750,
        widget=forms.TextInput(attrs={
            'type': 'search',
            'class': 'search-bar',
            'placeholder': 'Comidas, ingredientes, restaurantes...',
            })
    )

class PedidoForm(forms.Form):
    cantidad=forms.IntegerField(
        required=True,
        max_value=10,
        min_value=1,
        label="",
        initial=1,
        widget=forms.NumberInput(attrs={'step': '1'})
    )
    nota=forms.CharField(
        label="",
        initial="Vacio.",
        max_length=30,
        widget=forms.Textarea()
    )

class UbicacionForm(forms.Form):
    ubicacion=forms.CharField(
        required=True,
        label="Indique la ubicacion del pedido",
        max_length=50,
        widget=forms.TextInput()
    )
