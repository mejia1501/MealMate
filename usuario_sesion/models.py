from django.db import models
from django.utils import timezone
# Create your models here.
class Cliente(models.Model):
    username=models.CharField(max_length=150,default="")
    id=models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=40)
    password = models.CharField(max_length=18)
    cedula = models.CharField(max_length=8)
    email = models.EmailField(max_length=254)
    telefono = models.CharField(max_length=11)
    last_login = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    USERNAME_FIELD = 'username'  # Campo que se usará para el inicio de sesión
    REQUIRED_FIELDS = ['email']