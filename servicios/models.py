from django.db import models
from user_r.models import Restaurante
from django.utils import timezone
from datetime import date

# Create your models here.

class Reservaciones_config(models.Model):
    restaurante=models.ForeignKey(Restaurante,on_delete=models.CASCADE)
    mesas = models.CharField(max_length=500, blank=True, null=True,default='1,') #[5,2,7,2] la posicion es la mesa
    active= models.BooleanField(default=False)
    
class Reservaciones_horario(models.Model):
    restaurante=models.ForeignKey(Restaurante,on_delete=models.CASCADE)
    mesa = models.IntegerField(default=0)#nro de mesa
    fecha=models.DateField(default=date.today)#fecha
    horas=models.CharField(max_length=288)#horarios en esa fecha [12:00,12:30,4:00]

class Pickup_Delivery(models.Model):
    restaurante = models.ForeignKey(Restaurante, on_delete=models.CASCADE)
    p_start_time = models.TimeField(default=timezone.now)
    p_end_time = models.TimeField(default=timezone.now)
    active_pickup = models.BooleanField(default=False)
    d_start_time = models.TimeField(default=timezone.now)
    d_end_time = models.TimeField(default=timezone.now)
    active_delivery = models.BooleanField(default=False)

    