# myapp/templatetags/custom_filters.py

from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Obtiene el valor de un diccionario dado una clave."""
    return dictionary.get(key, '')