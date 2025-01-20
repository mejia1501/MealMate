from django.db import models
from user_r.models import Restaurante
from django.utils import timezone
from datetime import date

# Create your models here.

class Reservaciones_config(models.Model):
    restaurante=models.ForeignKey(Restaurante,on_delete=models.CASCADE)
    mesas = models.CharField(max_length=500, blank=True, null=True,default='1,') #[5,2,7,2] la posicion es la mesa
    active= models.BooleanField(default=False)#si el restaurante tiene reservaciones
    
class Reservaciones_horario(models.Model):
    restaurante=models.ForeignKey(Restaurante,on_delete=models.CASCADE)
    mesa = models.IntegerField(default=0)#nro de mesa
    fecha=models.DateField(default=date.today)#fecha
    horas=models.CharField(max_length=288)#horarios en esa fecha [12:00,12:30,4:00]
    status=models.CharField(max_length=144,default="")#indica que mesas estan ocupadas. 1=Si, 0=no [1,0,1,0,0....]

class Reservacion_cliente(models.Model):
    restaurante = models.ForeignKey(Restaurante, on_delete=models.CASCADE)
    nro_reserva=models.AutoField(primary_key=True)
    nombre=models.CharField(max_length=40)
    identificacion=models.CharField(max_length=20)
    email=models.EmailField(max_length=20)
    telefono=models.CharField(max_length=11)
    fecha=models.DateField(default=date.today)
    hora=models.TimeField(default=timezone.now)
    mesa=models.IntegerField(default=0)
    nro_personas=models.IntegerField(default=0)

class Pickup_Delivery(models.Model):
    restaurante = models.ForeignKey(Restaurante, on_delete=models.CASCADE)
    p_start_time = models.TimeField(default=timezone.now)
    p_end_time = models.TimeField(default=timezone.now)
    active_pickup = models.BooleanField(default=False)
    d_start_time = models.TimeField(default=timezone.now)
    d_end_time = models.TimeField(default=timezone.now)
    active_delivery = models.BooleanField(default=False)

    