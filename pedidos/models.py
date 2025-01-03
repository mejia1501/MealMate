from django.db import models
from django.utils import timezone
from user_r.models import Restaurante
# Create your models here.

class Pedido_Delivery(models.Model):
    id_nro=models.ForeignKey(Restaurante,on_delete=models.CASCADE)
    nro_items=models.CharField(max_length=200)
    fecha=models.DateTimeField(default=timezone.now)
    notas=models.CharField(max_length=500)
    cantidades=models.CharField(max_length=200)
    nombre = models.CharField(max_length=20)
    identificacion = models.CharField(max_length=20)
    email = models.EmailField(max_length=254)
    telefono = models.CharField(max_length=11)
    ubicacion=models.CharField(max_length=50,default='default')
    status=models.BooleanField(default=False)
    monto=models.FloatField(default=0)
    #nro de pedido
    nro=models.AutoField(primary_key=True)

class Pedido_Pickup(models.Model):
    #numero del pedido
    nro=models.AutoField(primary_key=True)
    #id del restaurante
    id_nro=models.ForeignKey(Restaurante,on_delete=models.CASCADE)
    nro_items=models.CharField(max_length=200)
    fecha=models.DateTimeField(default=timezone.now)
    notas=models.CharField(max_length=500)
    cantidades=models.CharField(max_length=200)
    nombre = models.CharField(max_length=40)
    identificacion = models.CharField(max_length=20)
    email = models.EmailField(max_length=254)
    telefono = models.CharField(max_length=11)
    monto=models.FloatField(default=0)
    ubicacion=models.CharField(max_length=50,default='default')
    status=models.BooleanField(default=False)

class PagoNacional(models.Model):
    id_nro=models.ForeignKey(Restaurante,on_delete=models.CASCADE)
    pedido=models.IntegerField(default=0)
    is_pagomovil = models.BooleanField(default=False)
    banco=models.CharField(max_length=4)
    monto=models.FloatField(default=0)
    ref=models.IntegerField()
    titular=models.CharField(max_length=40,default="")
    telefono=models.CharField(max_length=11,default="")
    is_efectivo = models.BooleanField(default=False)

class ZelleModel(models.Model):
    pedido=models.IntegerField()
    id_nro=models.ForeignKey(Restaurante,on_delete=models.CASCADE)
    monto=models.FloatField()
    ref=models.IntegerField()
    fecha=models.DateTimeField()
    titular=models.CharField(max_length=40)
    telefono=models.CharField(max_length=11)
    email = models.EmailField(max_length=254)

class PaypalModel(models.Model):
    pedido=models.IntegerField()
    id_nro=models.ForeignKey(Restaurante,on_delete=models.CASCADE)
    monto=models.FloatField()
    ref=models.IntegerField()
    fecha=models.DateTimeField()
    titular=models.CharField(max_length=40)
    email = models.EmailField(max_length=254)