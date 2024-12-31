from django.urls import path,include
from .import views
urlpatterns=[
    path('delivery/pedidos/detalles/<str:nro>/',views.DetailsDelivery,name='detail_delivery'),
    path('pago/<str:id>/<str:total>/',views.PagoView,name='pago'),
    path('datos_cliente/<str:id>/',views.Registro_datos_view,name='registro_datos'),
    path('pago_movil/<str:id>/',views.PagoMovilView,name='pago_movil'),
    path('pago/success/',views.SuccessView,name='success'),
    path('servicios/', include('servicios.urls')),
]