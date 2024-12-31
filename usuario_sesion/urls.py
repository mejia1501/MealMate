from django.urls import path,include
from . import views
urlpatterns=[
    path('login/',views.iniciar_sesion,name="login"),
    path('registro/cliente',views.registro_cliente,name="registro_cliente"),
    path('registro/restaurante',views.registro_restaurante,name="registro_restaurante"),
    path('perfil/',views.cuenta,name="perfil-cliente"),
    path('logout/',views.logout,name="logout"),
    path('perfil/edit/', views.ModificarCuenta, name='editar'),
    path('restaurante/', include('user_r.urls')),
]