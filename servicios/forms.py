from django import forms
from django.forms import ModelForm
from .models import Reservaciones_config,Pickup_Delivery


class CheckReserForm(ModelForm):
     class Meta:
        model = Reservaciones_config
        fields = ['active']
        widgets = { 
            'active': forms.CheckboxInput()
        }

class CheckPickForm(ModelForm):
     class Meta:
        model = Pickup_Delivery
        fields = ['active_pickup']
        widgets = { 
            'active_pickup': forms.CheckboxInput()
        }

class CheckDelivForm(ModelForm):
     class Meta:
        model = Pickup_Delivery
        fields = ['active_delivery']
        widgets = { 
            'active_delivery': forms.CheckboxInput()
        }