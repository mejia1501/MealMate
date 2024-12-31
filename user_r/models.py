from django.db import models
from django.utils import timezone

# Create your models here.

class Restaurante(models.Model):
    id=models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=20)
    password = models.CharField(max_length=18)
    rif = models.CharField(max_length=20)
    email = models.EmailField(max_length=254)
    telefono = models.CharField(max_length=11)
    direccion = models.CharField(max_length=200)
    fundacion = models.DateField()
    last_login = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    logo=models.CharField(max_length=100,default='default_logo.jpg')
    def __str__(self): return self.nombre

class Ingredientes(models.Model):
    codigo = models.AutoField(primary_key=True)
    ingrediente = models.CharField(max_length=20)
    def __str__(self): 
        return self.ingrediente
    
class Menu(models.Model):
    restaurante=models.ForeignKey(Restaurante,on_delete=models.CASCADE)
    comida = models.TextField(max_length=2750)
    precios = models.TextField(max_length=360)
    codigo = models.CharField(max_length=360)
    item=models.AutoField(primary_key=True)
    def __str__(self): return self.comida

class Pago(models.Model):
    restaurante=models.ForeignKey(Restaurante, on_delete=models.CASCADE)
    pagomovil_active = models.BooleanField(default=False)
    banco=models.CharField(max_length=4)
    telefono_pm= models.CharField(max_length=11)
    efectivo_active = models.BooleanField(default=False)
    #para ofrecer seguridad al cliente el rif del pago movil debe de ser el mismo con el que se registra la empresa

class Zelle(models.Model):
    restaurante=models.ForeignKey(Restaurante, on_delete=models.CASCADE)
    zelle_active = models.BooleanField(default=False) 
    mail_z= models.EmailField(max_length=254)
    phone_z=models.CharField(max_length=11)

class Paypal(models.Model):
    restaurante=models.ForeignKey(Restaurante, on_delete=models.CASCADE)
    paypal_active = models.BooleanField(default=False)
    nombre = models.CharField(max_length=20)
    user= models.CharField(max_length=20)
    correo = models.EmailField(max_length=254)
    phone_p=models.CharField(max_length=11,default=0)
