"""
URL configuration for project_admin project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from usuario_sesion import views as usuario_sesion_views
from user_r import views as user_r_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('usuario_sesion.urls')),
    path('restaurante/', include('user_r.urls')),
    path('servicios/', include('servicios.urls')),
    path('', include('principal.urls')),
    path('pedidos/', include('pedidos.urls')),
    path('perfil-cliente/', usuario_sesion_views.cuenta, name="perfil-cliente"),  # Perfil cliente
    path('perfil-restaurante/', user_r_views.cuenta, name="perfil-restaurante"),  # Perfil restaurante
    path('logout/', usuario_sesion_views.logout, name="logout"),
    path('login/', usuario_sesion_views.iniciar_sesion, name="login"),
    
]