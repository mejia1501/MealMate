from django.urls import path,include
from .import views
urlpatterns=[
    path('delivery/pedidos/detalles/<str:nro>/',views.DetailsDelivery,name='detail_delivery'),
    path('pickup/pedidos/detalles/<str:nro>/',views.DetailsPickup,name='detail_pickup'),

    path('fecha/',views.ReservacionesFechaView,name='reser_fecha'),
    path('horas/',views.ReservacionesHoraView,name='reser_hora'),

    path('pago/<str:id>/<str:total>/',views.PagoView,name='pago'),
    path('datos_cliente/<str:id>/',views.Registro_datos_view,name='registro_datos'),
    path('pago_movil/<str:id>/',views.PagoMovilView,name='pago_movil'),
    path('zelle/<str:id>/',views.ZellePagoView,name='zelle_pago'),
    path('efectivo/<str:id>/',views.EfectivoPagoView,name='pago_efectivo'),
    path('reservacion/reserva_cliente/<str:param1>/<int:param2>/<str:param3>/',views.VerReservaView,name='ver_reserva'),

    path('pago/success/',views.SuccessView,name='success'),
]