from django.urls import path,include
from . import views
urlpatterns=[
    path('reservaciones/',views.ActivateReserView,name="activate_r"),
    path('delivery/',views.ActivateDelivView,name='activate_d'),
    path('pickup/',views.ActivatePickView,name='activate_p'),
    path('delivery/pedidos/',views.DeliveryView,name='delivery'),
    path('pickup/pedidos/',views.PickupView,name='pickup'),
    path('reservaciones/mesas/',views.MesasView,name='mesas'),
    path('reservaciones/horarios_mesas/',views.HorariosMesasViews,name='horarios_mesas'),
    path('reservaciones/horarios_nuevo/',views.HorarioNew,name='horarios_nuevo'),
    path('reservaciones/modificar_reserva/<str:param1>/<int:param2>/<str:param3>/',views.ModificarReserva,name='modificar_reserva'),
    path('restaurante/', include('user_r.urls')),
]
