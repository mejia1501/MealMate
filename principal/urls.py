from django.urls import path,include
from .import views

urlpatterns=[
    path('',views.InicioView,name="home"),
    path('resultados/<str:texto>/',views.ResultadosView,name="resultados"),
    path('ayuda/',views.ayuda,name="ayuda"),
    path('restaurantes/menu_one/<str:item>/',views.DeliveryView,name='presentacion_one'),
    path('restaurantes/menu_three/<str:item>/',views.PickupView,name='presentacion_three'),
    path('restaurantes/menu_two/<str:item>/',views.Reservaciones,name='presentacion_two'),
    path('restaurantes/<str:item>/',views.PresentacionView,name='presentacion'),
    path('restaurantes/agregar_pedido/<int:id>/<str:item>/',views.Agregar_Pedido_View,name='agregar_pedido'),
    path('restaurantes/pedidos1/<str:item>/',views.PedidosView,name='pedidos'),
    path('restaurantes/modificar_pedido/<str:id>/<str:item>/',views.ModificarPedido,name='modificar_pedido'),
    #pickup
    path('restaurantes/agregar_pedido2/<str:id>/<str:item>/',views.Agregar_Pedido_View2,name='agregar_pedido2'),
    path('restaurantes/pedidos2/<str:item>/',views.PedidosView2,name='pedidos2'),
    path('restaurantes/modificar_pedido2/<str:id>/<str:item>/',views.ModificarPedido2,name='modificar_pedido2'),

    path('ubicacion/<str:id>/',views.UbicacionView,name='ubicacion'),
    path('restaurantes/eliminar_pedido/<str:key>/<str:id>/',views.EliminarPedidoView,name='eliminar_pedido'),
    
    path('ubicacion_restaurante/',views.UbicacionRestauranteView, name='ubicacion_restaurante'),
    path('user/',include('usuario_sesion.urls')),
    path('restaurante/', include('user_r.urls')),
    path('pedido/', include('pedidos.urls')),
]