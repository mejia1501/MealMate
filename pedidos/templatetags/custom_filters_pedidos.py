
from django import template

register = template.Library()

@register.filter
def add_one(value):
    return value + 1
@register.filter
def primeros_5(value):
    # Divide la cadena en palabras y selecciona las primeras 5
    return (value[:5])
