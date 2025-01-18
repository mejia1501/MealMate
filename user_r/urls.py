from django.urls import path,include
from . import views
from servicios.views import ActivateDelivView
urlpatterns=[
    path('',views.cuenta,name="perfil-restaurante"),
    path('editar',views.ModificarCuenta,name="editar-perfil"),
    path('menu',views.MostrarMenu,name="menu"),
    path('menu/crear',views.CrearMenu,name="crear_menu"),
    path('menu/editar/<str:item>/',views.ModificarMenu,name="editar_menu"),
    path('menu/editar/delete/<str:item>/',views.DeleteDish,name="delete_dish"),
    path('menu/crear/crear_ingrediente/<str:nro>/',views.NuevoIngrediente,name="add_ingrediente"),
    path('servicios/activate_d',ActivateDelivView,name='activate_d'),
    path('pago_nacional',views.PagoNacional,name="pago_nacional"),
    path('paypal',views.PaypalView,name="paypal"),
    path('zelle',views.ZelleView,name="zelle"),
]
