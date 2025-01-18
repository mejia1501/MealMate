from django.db import models
from django.utils import timezone
# Create your models here.
class Cliente(models.Model):
    id=models.AutoField(primary_key=True)
    username=models.CharField(max_length=18)
    nombre = models.CharField(max_length=40)
    password1 = models.CharField(max_length=18,default="")
    password2 = models.CharField(max_length=18,default="")
    cedula = models.CharField(max_length=8)
    email = models.EmailField(max_length=254)
    telefono = models.CharField(max_length=11)
    last_login = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)