from django.shortcuts import render,redirect
from django.urls import reverse
from django.core.paginator import Paginator
from user_r.models import Restaurante,Menu,Ingredientes,Pago,Paypal,Zelle
from servicios.models import Reservaciones_config,Pickup_Delivery
from .forms import BarraBusqueda,PedidoForm,UbicacionForm
from pedidos.views import cambio_dolar
from geopy.distance import great_circle
#pip install geopy
from geopy import distance
from geopy.geocoders import Nominatim
from django.utils import timezone
import pytz #pip install pytz
from datetime import datetime
zona_horaria = pytz.timezone('America/Caracas')
# Create your views here.
def ayuda(request):
    return render(request,'ayuda.html')



def InicioView(request):

    if request.method == "GET":
        return render(request, 'home.html', {
            'busqueda': BarraBusqueda(),
            'inicio': 'MealMate',
        })
    else:
        request.session.pop('ubicacion', None)
        form = BarraBusqueda(request.POST)
        if 'ubicacion'  not in request.session and form.is_valid():
            request.session['busqueda'] = form.cleaned_data['texto']
            return redirect('ubicacion',id=0)
        
        elif form.is_valid():
            search = form.cleaned_data['texto'].lower()
            return redirect('resultados',texto=search)
        else:
            return render(request, 'home.html', {
                'busqueda': BarraBusqueda(),
                'error': 'Por favor, corrige los errores en el formulario.'
            })

def ResultadosView(request,texto):
    if request.method=="GET":
        try:
            # Obtener el valor del campo del formulario
            search = str(texto)
            resultados = {}  #  diccionario para almacenar los resultados
            cliente = request.session.get('ubicacion')
            cliente = cliente.split('+')
            cliente = (cliente[0], cliente[1])  # Asegúrate de que haya al menos dos elementos

# Buscar coincidencias exactas en 'Menu'
            comidas = Menu.objects.filter(comida=search).values('comida','restaurante')
            if comidas.exists():
                for comida in comidas:
                    restaurante = Restaurante.objects.filter(id=comida['restaurante']).first()
                    mail = request.session.get('email')
                    if restaurante:
                        # Procesar la dirección del restaurante
                        direccion_r = restaurante.direccion.split("+")
                        direccion_r = (direccion_r[0], direccion_r[1])  # Asegúrate de que haya al menos dos elementos
                        
                        # Si el restaurante no es del usuario, mostrar los resultados
                        if restaurante.email != mail:
                            reservacion = Reservaciones_config.objects.filter(restaurante=restaurante.id).first()
                            pandd = Pickup_Delivery.objects.filter(restaurante=restaurante.id).first()
                            ubicacion=obtener_direccion(direccion_r[0], direccion_r[1])

                            # Usar el ID del restaurante como clave en el diccionario
                            resultados[restaurante.id] = {
                                'comida': comida['comida'],
                                'restaurante_nombre': restaurante.nombre,
                                'ubicacion': ubicacion,
                                'id':restaurante.id,
                                'delivery': pandd.active_delivery if pandd else False,
                                'pickup': pandd.active_pickup if pandd else False,
                                'reservaciones': reservacion.active if reservacion else False,
                                'distancia': round(distance.great_circle(direccion_r, cliente).km,2),
                            }                            
            else:
                # Buscar coincidencias en 'Ingredientes'
                ingredientes = Menu.objects.all()
                for ingredient in ingredientes:
                    lista = ingredient.codigo.split(',')
                    for codigo in lista:
                        # Buscar el código en la tabla ingredientes y sustituirlo por su palabra correspondiente
                        word = Ingredientes.objects.filter(codigo=codigo).first()
                        if word and search.lower() == word.ingrediente.lower():
                            # Si coincide con la barra de búsqueda
                            restaurante = Restaurante.objects.filter(id=ingredient.restaurante_id).first()
                            direccion_r = restaurante.direccion.split("+")
                            direccion_r = (direccion_r[0], direccion_r[1])  # Asegúrate de que haya al menos dos elementos
                            mail = request.session.get('email')
                            # Si el restaurante no es del usuario, añadir a resultados
                            if restaurante and restaurante.email != mail:
                                reservacion = Reservaciones_config.objects.filter(restaurante=restaurante.id).first()
                                pandd = Pickup_Delivery.objects.filter(restaurante=restaurante.id).first()

                                # Procesar la dirección del restaurante
                                direccion_r = restaurante.direccion.split("+")
                                direccion_r = (direccion_r[0], direccion_r[1])  # Asegúrate de que haya al menos dos elementos
                                
                                ubicacion=obtener_direccion(direccion_r[0], direccion_r[1])
                                # Usar el ID del restaurante como clave en el diccionario
                                resultados[restaurante.id] = {
                                    'restaurante_nombre': restaurante.nombre,
                                    'ubicacion': ubicacion,
                                    'id':restaurante.id,
                                    'delivery': pandd.active_delivery if pandd else False,
                                    'pickup': pandd.active_pickup if pandd else False,
                                    'reservaciones': reservacion.active if reservacion else False,
                                    'distancia': round(distance.great_circle(direccion_r, cliente).km,2),
                                }
            print(resultados)
                # Eliminar duplicados usando unique_everseen 
            resultados_lista = list(resultados.values())
            resultados_lista=sorted(resultados_lista, key=lambda x: x['distancia'])
            # Paginación
            paginator = Paginator(resultados_lista, 10)
            pagina = request.GET.get("page") or 1
            items = paginator.get_page(pagina)
            pagina_actual = int(pagina)
            paginas = range(1, items.paginator.num_pages + 1)

            return render(request, 'resultados.html', {
                    'busqueda': BarraBusqueda(),
                    'items': items,
                    'paginas': paginas,
                    'pagina_actual': pagina_actual,
            })
        except Exception as e:
            return render(request, 'resultados.html', {
                'busqueda': BarraBusqueda(),
                'error': f'{e}'
            })
    else:
        form = BarraBusqueda(request.POST)
        if 'ubicacion'  not in request.session:
            return redirect('ubicacion',id=0)
        
        elif form.is_valid():
            search = form.cleaned_data['texto'].lower()
            return redirect('resultados',texto=search)
        else:
            return render(request, 'resultados.html', {
                'busqueda': BarraBusqueda(),
                'error': 'Por favor, corrige los errores en el formulario.'
            })

def PresentacionView(request,item):
    if request.method == 'GET':
        try:
            restaurante = Restaurante.objects.filter(id=item).first()
            reservacion = Reservaciones_config.objects.filter(restaurante=restaurante.id).first()
            pandd = Pickup_Delivery.objects.filter(restaurante=restaurante.id).first()  

            return render(request, 'presentacion.html', {
                'restaurante': restaurante,
                'delivery': pandd.active_delivery if pandd else False,
                'pickup': pandd.active_pickup if pandd else False,
                'reservaciones': reservacion.active if reservacion else False
            })
        except Restaurante.DoesNotExist:
            return render(request, 'presentacion.html', {
                'error': "El restaurante no se encontró.",
            })
        except Exception as e:
            return render(request, 'presentacion.html', {
                'error': f"Que extraño, no hay coincidencias. Recargue la página por favor. Error: {e}"
            })

def DeliveryView(request, item):
    try:
        item = int(item)          
        if 'restaurante' in request.session:
            restaurante_sesion = request.session.get('restaurante')
            restaurante_sesion = int(restaurante_sesion)
        else:
            request.session['restaurante']=item
            restaurante_sesion = request.session.get('restaurante')
            restaurante_sesion = int(restaurante_sesion)

        restaurante = Restaurante.objects.get(id=item)
        if request.method == 'GET':
            # Si el pedido que se estaba llenando no era del mismo restaurante, vaciar las variables de sesión
            if restaurante_sesion != int(restaurante.id):
                print('funciona')
                # Guardar el valor de la variable que deseas conservar
                valor_a_conservar = request.session.get('email')
                ubicacion = request.session.get('ubicacion')
                timestamp=request.session.get('timestamp')
             #vaciar todas las variables de sesión
                request.session.flush()

                # Restaurar la variable que deseas conservar
                request.session['email'] = valor_a_conservar
                request.session['ubicacion'] = ubicacion
                request.session['timestamp'] = timestamp

            # Verificar si la ubicación está en la sesión
            if not request.session.get("ubicacion"):
                return redirect("ubicacion", id=item)
            else:
                if restaurante.direccion:
                    coordenadas = restaurante.direccion.split('+')
                    ubicacion_restaurante = obtener_direccion(coordenadas[0], coordenadas[1])
                    latitud = str(coordenadas[0])
                    longitud = str(coordenadas[1])
                
# Obtener la reservación y la hora actual
                reservacion = Reservaciones_config.objects.filter(restaurante=restaurante.id).first()
                hora_actual = datetime.now(zona_horaria).strftime('%H:%M')
                pandd = Pickup_Delivery.objects.filter(restaurante=restaurante.id).first()  
                menu = Menu.objects.filter(restaurante=item)

                # Obtener la ubicación del restaurante
                ubicacion_restaurante = restaurante.direccion.split('+')
                print(ubicacion_restaurante)
                restaurante_u = (ubicacion_restaurante[0], ubicacion_restaurante[1])
                cliente = request.session.get("ubicacion")
                
                cliente = cliente.split("+")
                cliente = (cliente[0], cliente[1])
                print(cliente)

                # Calcular la distancia
                distancia = round(great_circle(restaurante_u, cliente).km, 2)

                # Verificar condiciones de entrega
                error = None
                pandd.d_end_time=pandd.d_end_time.strftime('%H:%M')
                pandd.d_start_time=pandd.d_start_time.strftime('%H:%M')

                if float(distancia) > float(ubicacion_restaurante[2]):
                    error = f'Estimado cliente, lamentamos informarle que este restaurante no acepta pedidos de entrega a domicilio para ubicaciones que superen una distancia de {ubicacion_restaurante[2]} km.'
                elif hora_actual > pandd.d_end_time or hora_actual < pandd.d_start_time:
                    error = f'Estimado cliente, lamentamos informarle que el servicio de entrega a domicilio de este restaurante finaliza a las {pandd.d_end_time} y se reanuda a las {pandd.d_start_time}.'
              
                # Renderizar la respuesta
                if error:
                    return render(request, 'delivery.html', {
                        'error': error,
                        'delivery': pandd.active_delivery if pandd else False,
                        'pickup': pandd.active_pickup if pandd else False,
                        'reservaciones': reservacion.active if reservacion else False,
                        'restaurante': restaurante,
                        'id': str(restaurante.id),
                        'latitud': latitud,
                        'longitud': longitud,
                    })
                else:  
                    ubicacion_restaurante = obtener_direccion(ubicacion_restaurante[0], ubicacion_restaurante[1])

                    for menu_item in menu:
                        menu_item.codigo = obtener_ingredientes(menu_item.codigo)

                    activo = 'elegidos' in request.session and request.session.get('elegidos') != ""
                   

                    return render(request, 'delivery.html', {
                        'restaurante': restaurante, 
                        'menu': menu,
                        'ubicacion_restaurante': ubicacion_restaurante,
                        'ubicacion': obtener_direccion(cliente[0],cliente[1]),
                        'id': str(restaurante.id),
                        'form': PedidoForm(),
                        'delivery': pandd.active_delivery if pandd else False,
                        'pickup': pandd.active_pickup if pandd else False,
                        'reservaciones': reservacion.active if reservacion else False,
                        'activo': activo,
                        'latitud': latitud,
                        'longitud': longitud,
                    })

    except Exception as e:
        return render(request, 'delivery.html', {
            'error': f"Que extraño, no hay coincidencias. Recargue la página por favor. Error: {e}",
            'id': item,
        })
    
def PickupView(request, item):
    item = int(item)          
    if 'restaurante' in request.session:
        restaurante_sesion = request.session.get('restaurante')
        restaurante_sesion = int(restaurante_sesion)
    else:
        request.session['restaurante']=item
        restaurante_sesion = request.session.get('restaurante')
        restaurante_sesion = int(restaurante_sesion)
    try:
        restaurante = Restaurante.objects.get(id=item)

        if request.method == 'GET':
            # Si el pedido que se estaba llenando no era del mismo restaurante, vaciar las variables de sesión
            if restaurante_sesion  != int(restaurante.id):
                # Guardar el valor de la variable que deseas conservar
                valor_a_conservar = request.session.get('email')
                ubicacion = request.session.get('ubicacion')
                timestamp=request.session.get('timestamp')
             #vaciar todas las variables de sesión
                request.session.flush()

                # Restaurar la variable que deseas conservar
                request.session['email'] = valor_a_conservar
                request.session['ubicacion'] = ubicacion
                request.session['timestamp'] = timestamp
            if restaurante.direccion:
                coordenadas = restaurante.direccion.split('+')
                ubicacion_restaurante = obtener_direccion(coordenadas[0], coordenadas[1])
                latitud = str(coordenadas[0])
                longitud = str(coordenadas[1])
            else:
                ubicacion_restaurante = None
                latitud = longitud = None  # Manejar el caso en que no haya dirección
            # Obtener el restaurante y otros datos
            reservacion = Reservaciones_config.objects.filter(restaurante=restaurante.id).first()
            pandd = Pickup_Delivery.objects.filter(restaurante=restaurante.id).first()  
            menu = Menu.objects.filter(restaurante=item)
            hora_actual = datetime.now(zona_horaria).strftime('%H:%M')
            error = None
            pandd.p_end_time=pandd.p_end_time.strftime('%H:%M')
            pandd.p_start_time=pandd.p_start_time.strftime('%H:%M')
            print(hora_actual)
            if hora_actual > pandd.p_end_time or hora_actual < pandd.p_start_time:
                error = f'Estimado cliente, lamentamos informarle que el servicio de pickup de este restaurante finaliza a las {pandd.p_end_time} y se reanuda a las {pandd.p_start_time}.'
              
            # Renderizar la respuesta
            if error:
                return render(request, 'pickup.html', {
                    'error': error,
                    'delivery': pandd.active_delivery if pandd else False,
                        'pickup': pandd.active_pickup if pandd else False,
                        'reservaciones': reservacion.active if reservacion else False,
                        'restaurante': restaurante,
                        'id': str(restaurante.id),
                        'latitud': latitud,
                        'longitud': longitud,
                })
                    
            else:
                for menu_item in menu:
                    menu_item.codigo = obtener_ingredientes(menu_item.codigo)

                activo = 'elegidos2' in request.session

                # Manejo de coordenadas
                return render(request, 'pickup.html', {
                    'ubicacion_restaurante': ubicacion_restaurante,
                    'restaurante': restaurante, 
                    'menu': menu,
                    'id': restaurante.id,
                    'delivery': pandd.active_delivery if pandd else False,
                    'pickup': pandd.active_pickup if pandd else False,
                    'reservaciones': reservacion.active if reservacion else False,
                    'activo': activo,
                    'latitud': latitud,
                    'longitud': longitud,
                })

    except Restaurante.DoesNotExist:
        return render(request, 'pickup.html', {
            'error': "El restaurante no se encontró.",
        })
    except Exception as e:
        return render(request, 'pickup.html', {
            'error': f"Que extraño, no hay coincidencias. Recargue la página por favor. Error: {e}",
        })

    # Manejo de otros métodos (por ejemplo, POST)
    return render(request, 'pickup.html', {
        'error': "Método no permitido.",
    })

def Reservaciones(request, item):
    if request.method == 'GET':
        item=int(item)
        request.session['restaurante']=item
        id=int(request.session.get('restaurante'))
        if id!=item:
            valor_a_conservar = request.session.get('email')
            ubicacion = request.session.get('ubicacion')
            timestamp=request.session.get('timestamp')
             #vaciar todas las variables de sesión
            request.session.flush()

                # Restaurar la variable que deseas conservar
            request.session['email'] = valor_a_conservar
            request.session['ubicacion'] = ubicacion
            request.session['timestamp'] = timestamp
            
        restaurante = Restaurante.objects.filter(id=item).first()
        if not restaurante:
            raise Restaurante.DoesNotExist
                
        reservacion = Reservaciones_config.objects.filter(restaurante=restaurante.id).first()
        pandd = Pickup_Delivery.objects.filter(restaurante=restaurante.id).first()  

        reservacion.mesas = reservacion.mesas.split(',')
        reservacion.mesas = [int(valor) for valor in reservacion.mesas if valor.isdigit()]  
        # Obtener la mesa mayor
        mayor = max(reservacion.mesas)
        if restaurante.direccion!="":
            coordenadas=restaurante.direccion.split('+')
            ubicacion_restaurante=obtener_direccion(coordenadas[0],coordenadas[1])
        return render(request, 'reservaciones_s.html', {
                    'ubicacion_restaurante': ubicacion_restaurante,
                    'restaurante': restaurante,
                    'delivery': pandd.active_delivery if pandd else False,
                    'pickup': pandd.active_pickup if pandd else False,
                    'reservaciones': reservacion.active if reservacion else False,
                    'mayor':mayor,
                    'personas': list(range(1, mayor + 1)),
                    'latitud': str(coordenadas[0]),
                    'longitud': str(coordenadas[1]),
        })
    elif request.method == 'POST':
        
        personas=request.POST.get('personas')
        print("PERSONAS: ",personas)
        if personas:
            request.session['restaurante']=item
            request.session['reservacion']=True
            request.session['puestos']=personas
            request.session.save()
            return redirect('reser_fecha')
        else:
            return render(request, 'reservaciones_s.html', {
                    'error': "Revise el formulario",
                })
        
def Agregar_Pedido_View(request, id, item):
    if request.method == 'GET':
        try:
            restaurante = Restaurante.objects.get(id=id)
            menu = Menu.objects.filter(restaurante=restaurante.id, item=item).first()

            if menu is None:
                return render(request, 'agregar_pedido.html', {
                    'error': "El menú no se encontró.",
                })

            menu.codigo = obtener_ingredientes(menu.codigo)
            return render(request, 'agregar_pedido.html', {
                'menu': menu,
                'restaurante': restaurante,
                'form': PedidoForm(),
            })
        except Restaurante.DoesNotExist:
            return render(request, 'agregar_pedido.html', {
                'error': "El restaurante no se encontró.",
            })
        except Exception as e:
            return render(request, 'agregar_pedido.html', {
                'error': f"Que extraño, no hay coincidencias. Recargue la página por favor. Error: {e}"
            })
        
    elif request.method == 'POST':
        
        form = PedidoForm(request.POST)
        if form.is_valid():

            # Para saber qué restaurante traer los medios de pago
            restaurante = Restaurante.objects.filter(id=id).first()
            if not restaurante:
                return render(request, 'delivery.html', {
                    'error': "El restaurante no se encontró.",
                })
            else:
               
                #True=pickup, False=delivery
                request.session['type']=False
                # Almacenar en la sesión
                request.session['restaurante'] = restaurante.id
                request.session[f'comentario_{item}'] = form.cleaned_data['nota']

                # Items elegidos
                elegidos_actual = request.session.get('elegidos', '')
                nuevos_elegidos = item

                # Concatenar el nuevo contenido al valor existente
                if elegidos_actual:
                    nuevo_valor = f"{elegidos_actual},{nuevos_elegidos}"
                else:
                    nuevo_valor = nuevos_elegidos

                # Almacenar en la sesión
                request.session['elegidos'] = nuevo_valor

                # Cantidad
                cantidad_actual = request.session.get('cantidad', '')
                nuevos = form.cleaned_data['cantidad']

                # Concatenar el nuevo contenido al valor existente
                if cantidad_actual:
                    nuevo_valor_cantidad = f"{cantidad_actual},{nuevos}"
                else:
                    nuevo_valor_cantidad = nuevos

                # Almacenar en la sesión
                request.session['cantidad'] = nuevo_valor_cantidad

                return redirect('presentacion_one', item=id)
        else:
            return render(request, 'agregar_pedido.html', {
                'form': form,
                'error': "Revise el formulario.",
            })

def PedidosView(request,item):
    
    restaurante = Restaurante.objects.filter(id=item).first()
    if 'total' in request.session:
        del request.session['total']
    if not restaurante:
        return render(request, 'pedidos.html', {
            'error': 'Restaurante no encontrado',
        })

    if request.method == "GET":
        #False=delivery,True=pickup
        request.session['type']=False
      # Recuperar las variables de sesión
        elegidos = request.session.get('elegidos', 'No disponible')
        cantidad = request.session.get('cantidad', 'No disponible')

        # Verificar si 'elegidos' y 'cantidad' son válidos
        if elegidos == 'No disponible' or cantidad == 'No disponible':
            return render(request, 'pedidos.html', {
                'error': 'No hay elementos disponibles en la sesión.',
            })

        # Verificar si 'elegidos' tiene un solo elemento
        if ',' not in str(elegidos):
            elegidos = [elegidos]  # Convertir a lista con un solo elemento
        else:
            elegidos = elegidos.split(',')  # Dividir en lista

        # Hacer lo mismo para 'cantidad'
        if ',' not in str(cantidad):
            cantidad = [cantidad]  # Convertir a lista con un solo elemento
        else:
            cantidad = cantidad.split(',')  # Dividir en lista

        # Crear un diccionario para almacenar los detalles de los ítems
        detalles_items = {}

        # Iterar sobre los elegidos y sus cantidades
        for i in range(len(elegidos)):
            elegido = elegidos[i]
            comida = Menu.objects.filter(item=elegido, restaurante=restaurante.id).first()
            cant = cantidad[i] if i < len(cantidad) else '0'  # Asegurarse de que la cantidad exista

            # Recuperar el comentario correspondiente
            comentario = request.session.get(f'comentario_{elegido}', 'No disponible')

            if comida:  # Verificar que comida no sea None
                # Agregar los detalles a la lista
                bolivar=cambio_dolar(float(comida.precios) * float(cant))
                detalles_items[i] = {
                    'item': elegido,
                    'comida': comida.comida,
                    'ingredientes': obtener_ingredientes(comida.codigo),
                    'precio': float(comida.precios),  # Asegúrate de que sea float
                    'cantidad': float(cant),  # Asegúrate de que sea float
                    'comentario': comentario,
                    'total': float(comida.precios) * float(cant),
                    'bolivar': round(float(bolivar),2),
                }
            else:
                # Manejar el caso donde no se encuentra la comida
                detalles_items[i] = {
                    'item': elegido,
                    'comida': 'No disponible',
                    'ingredientes': [],
                    'precio': 0,
                    'cantidad': float(cant),  # Asegúrate de que sea float
                    'comentario': comentario,
                    'total': 0,
                    'bolivar':0,
                }

        # Calcular el total y el IVA
        total = sum(item['total'] for item in detalles_items.values())  # Sumar todos los totales
        iva = total + (total * 0.16)  # Total con IVA
        bolivares=cambio_dolar(iva)
        # Redondear los valores a dos decimales
        total = round(total, 2)
        iva = round(iva, 2)
        ubicacion=request.session.get("ubicacion")
        ubicacion=ubicacion.split("+")
        request.session['total']=iva
        return render(request, 'pedidos.html', {
            'pedidos_dict': detalles_items,
            'restaurante': restaurante.nombre,
            'id': str(restaurante.id),
            'ubicacion':obtener_direccion(ubicacion[0], ubicacion[1]),
            'total': str(total),
            'iva': iva,
            'bolivares': round(float(bolivares),2),
        })

def ModificarPedido(request, id, item):
    id = str(id)
    restaurante = Restaurante.objects.filter(id=id).first()
    
    # Verificar si el restaurante existe
    if not restaurante:
        return render(request, 'modificar_pedido.html', {
            'error': 'Restaurante no encontrado',
        })

    if request.method == "GET":
        # Recuperar las variables de sesión
        elegidos = request.session.get('elegidos', 'No disponible')
        cantidad = request.session.get('cantidad', '0')  # Cambiar a '0' por defecto

        # Convertir a listas
        items = elegidos.split(',') if ',' in str(elegidos) else [elegidos]
        cantidad_list = cantidad.split(',') if ',' in str(cantidad) else [cantidad]

        # Crear una lista para almacenar los detalles de los ítems
        detalles_items = []

        # Iterar sobre los elegidos y sus cantidades
        for j, elegido in enumerate(items):
            if elegido == item:  # Asegúrate de que 'item' esté definido en el contexto
                comida = Menu.objects.filter(item=elegido, restaurante=restaurante.id).first()
                cant = cantidad_list[j] if j < len(cantidad_list) else '0'  # Asegurarse de que la cantidad exista

                # Recuperar el comentario correspondiente
                comentario = request.session.get(f'comentario_{elegido}', 'No disponible')

                if comida:  # Verificar que comida no sea None
                    # Agregar los detalles a la lista
                    detalles_items.append({
                        'item': elegido,
                        'comida': comida.comida,
                        'ingredientes': obtener_ingredientes(comida.codigo),
                        'precio': comida.precios,
                        'cantidad': cant,
                        'comentario': comentario,
                        'total': float(comida.precios) * float(cant),
                    })
                else:
                    # Manejar el caso donde no se encuentra la comida
                    detalles_items.append({
                        'item': elegido,
                        'comida': 'No disponible',
                        'ingredientes': [],
                        'precio': 0,
                        'cantidad': cant,
                        'comentario': comentario,
                        'total': 0,
                    })

        return render(request, 'modificar_pedido.html', {
            'pedidos_dict': detalles_items,
            'restaurante': restaurante.nombre,
            'item': str(restaurante.id),
        })

    elif request.method == "POST":
        # Obtener el item que estamos cambiando
        item = request.POST.get('item')
        comentario_nuevo = request.POST.get('comentario')
        cantidad_nueva = request.POST.get('cantidad')

        try:
            # Items elegidos
            elegidos_actual = request.session.get('elegidos', '')
            cantidad_actual = request.session.get('cantidad', '')

            # Convertir a listas
            elegidos_actual = elegidos_actual.split(',') if ',' in str(elegidos_actual) else [elegidos_actual]
            cantidad_actual = cantidad_actual.split(',') if ',' in str(cantidad_actual) else [cantidad_actual]

            # Verificar si el item está en elegidos
            if item in elegidos_actual:
                # Obtener el índice del item
                index = elegidos_actual.index(item)
                
                # Actualizar el comentario y la cantidad
                request.session[f'comentario_{item}'] = comentario_nuevo
                cantidad_actual[index] = cantidad_nueva  # Actualiza la cantidad en la posición correspondiente

                # Almacenar en la sesión
                request.session['cantidad'] = ",".join(cantidad_actual)  # Guarda la lista actualizada
                return redirect('pedidos', item=id)  # Redirige correctamente a la vista 'pedidos'
            else:
                raise ValueError("El item no está en la lista de elegidos.")

        except ValueError as ve:
            return render(request, 'modificar_pedido.html', {
                'error': str(ve),
                 'item': str(restaurante.id),
            })
        except Exception as e:
            return render(request, 'modificar_pedido.html', {
                'error': f"Ocurrió un error inesperado.{e}",
                'item': str(restaurante.id),
            })
  #pickup  
       
def Agregar_Pedido_View2(request, id, item):
    if request.method == 'GET':
        try:
            restaurante = Restaurante.objects.get(id=id)
            menu = Menu.objects.filter(restaurante=restaurante.id, item=item).first()

            if menu is None:
                return render(request, 'agregar_pedido2.html', {
                    'error': "El menú no se encontró.",
                })

            menu.codigo = obtener_ingredientes(menu.codigo)
            return render(request, 'agregar_pedido2.html', {
                'menu': menu,
                'restaurante': restaurante,
                'form': PedidoForm(),
            })
        except Restaurante.DoesNotExist:
            return render(request, 'agregar_pedido2.html', {
                'error': "El restaurante no se encontró.",
            })
        except Exception as e:
            return render(request, 'agregar_pedido2.html', {
                'error': f"Que extraño, no hay coincidencias. Recargue la página por favor. Error: {e}"
            })
        
    elif request.method == 'POST':
        
        form = PedidoForm(request.POST)
        if form.is_valid():

            # Para saber qué restaurante traer los medios de pago
            restaurante = Restaurante.objects.filter(id=id).first()
            if not restaurante:
                return render(request, 'pickup.html', {
                    'error': "El restaurante no se encontró.",
                })
            else:
                request.session['restaurante']=id
                #True=pickup, False=delivery
                request.session['type']=True
                # Almacenar en la sesión
                request.session[f'2comentario_{item}'] = form.cleaned_data['nota']

                # Items elegidos
                elegidos_actual = request.session.get('elegidos2', '')
                nuevos_elegidos = item

                # Concatenar el nuevo contenido al valor existente
                if elegidos_actual:
                    nuevo_valor = f"{elegidos_actual},{nuevos_elegidos}"
                else:
                    nuevo_valor = nuevos_elegidos

                # Almacenar en la sesión
                request.session['elegidos2'] = nuevo_valor

                # Cantidad
                cantidad_actual = request.session.get('cantidad2', '')
                nuevos = form.cleaned_data['cantidad']

                # Concatenar el nuevo contenido al valor existente
                if cantidad_actual:
                    nuevo_valor_cantidad = f"{cantidad_actual},{nuevos}"
                else:
                    nuevo_valor_cantidad = nuevos

                # Almacenar en la sesión
                request.session['cantidad2'] = nuevo_valor_cantidad

                return redirect('presentacion_three', item=id)
        else:
            return render(request, 'agregar_pedido2.html', {
                'form': form,
                'error': "Revise el formulario.",
            })

def PedidosView2(request,item):
    
    restaurante = Restaurante.objects.filter(id=item).first()
    request.session['type']=True
    if not restaurante:
        return render(request, 'pedidos2.html', {
            'error': 'Restaurante no encontrado',
        })

    if request.method == "GET":
        # Recuperar las variables de sesión
        elegidos = request.session.get('elegidos2', 'No disponible')
        if elegidos=="":
            return redirect('presentacion_three',item)
        cantidad = request.session.get('cantidad2', 'No disponible')

        # Verificar si 'elegidos' y 'cantidad' son válidos
        if elegidos == 'No disponible' or cantidad == 'No disponible':
            return render(request, 'pedidos2.html', {
                'id': str(restaurante.id),
                'iva': 0,
                'error': 'No hay elementos disponibles en la sesión.',
            })

        # Verificar si 'elegidos' tiene un solo elemento
        if ',' not in str(elegidos):
            elegidos = [elegidos]  # Convertir a lista con un solo elemento
        else:
            elegidos = elegidos.split(',')  # Dividir en lista

        # Hacer lo mismo para 'cantidad'
        if ',' not in str(cantidad):
            cantidad = [cantidad]  # Convertir a lista con un solo elemento
        else:
            cantidad = cantidad.split(',')  # Dividir en lista

        # Crear un diccionario para almacenar los detalles de los ítems
        detalles_items = {}

        # Iterar sobre los elegidos y sus cantidades
        for i in range(len(elegidos)):
            elegido = elegidos[i]
            comida = Menu.objects.filter(item=elegido, restaurante=restaurante.id).first()
            cant = cantidad[i] if i < len(cantidad) else '0'  # Asegurarse de que la cantidad exista

            # Recuperar el comentario correspondiente
            comentario = request.session.get(f'2comentario_{elegido}', 'No disponible')

            if comida:  # Verificar que comida no sea None
                bolivar=cambio_dolar(float(comida.precios) * float(cant))
                # Agregar los detalles a la lista
                detalles_items[i] = {
                    'item': elegido,
                    'comida': comida.comida,
                    'ingredientes': obtener_ingredientes(comida.codigo),
                    'precio': float(comida.precios),  # Asegúrate de que sea float
                    'cantidad': float(cant),  # Asegúrate de que sea float
                    'comentario': comentario,
                    'total': float(comida.precios) * float(cant),
                    'bolivar': round(float(bolivar),2),
                }
            else:
                # Manejar el caso donde no se encuentra la comida
                detalles_items[i] = {
                    'item': elegido,
                    'comida': 'No disponible',
                    'ingredientes': [],
                    'precio': 0,
                    'cantidad': float(cant),  # Asegúrate de que sea float
                    'comentario': comentario,
                    'total': 0,
                    'bolivar':0,
                }

        # Calcular el total y el IVA
        
        total = sum(item['total'] for item in detalles_items.values())  # Sumar todos los totales
        iva = total + (total * 0.16)  # Total con IVA
        bolivares=cambio_dolar(iva)

        # Redondear los valores a dos decimales
        total = round(total, 2)
        iva = round(iva, 2)
        request.session['total']=iva

        return render(request, 'pedidos2.html', {
            'pedidos_dict': detalles_items,
            'restaurante': restaurante.nombre,
            'id': str(restaurante.id),
            'total': total,
            'iva': iva,
            'bolivares': round(float(bolivares),2),
        })

def ModificarPedido2(request, id, item):
    restaurantes = Restaurante.objects.filter(id=id).first()
        # Verificar si el restaurante existe
    if not restaurantes:
        return render(request, 'modificar_pedido2.html', {
            'error': 'Restaurante no encontrado',
    })
           # Recuperar las variables de sesión
    elegidos = request.session.get('elegidos2', 'No disponible')
    cantidad = request.session.get('cantidad2', 'No disponible')
    elegidos=str(elegidos)
    cantidad=str(cantidad)
     
    if ',' not in str(elegidos):
        items = [elegidos]  # Convertir a lista con un solo elemento
    else:
        items = elegidos.nro_items.split(',')  # Dividir en lista
        
    if ',' not in str(cantidad):
        cantidad_list = [cantidad]  # Convertir a lista con un solo elemento
    else:
        cantidad_list = cantidad.split(',')  # Dividir en lista

    if request.method == "GET":
        

        # Crear una lista para almacenar los detalles de los ítems
        detalles_items = []

        # Iterar sobre los elegidos y sus cantidades
        for j, elegido in enumerate(items):
            if elegido == item:  # Asegúrate de que 'item' esté definido en el contexto
                comida = Menu.objects.filter(item=elegido, restaurante=restaurantes.id).first()
                cant = cantidad_list[j] if j < len(cantidad_list) else '0'  # Asegurarse de que la cantidad exista

                # Recuperar el comentario correspondiente
                comentario = request.session.get(f'2comentario_{elegido}', 'No disponible')

                if comida:  # Verificar que comida no sea None
                    # Agregar los detalles a la lista
                    detalles_items.append({
                        'item': elegido,
                        'comida': comida.comida,
                        'ingredientes': obtener_ingredientes(comida.codigo),
                        'precio': comida.precios,
                        'cantidad': cant,
                        'comentario': comentario,
                        'total': float(comida.precios) * float(cant),
                    })
                else:
                    # Manejar el caso donde no se encuentra la comida
                    detalles_items.append({
                        'item': elegido,
                        'comida': 'No disponible',
                        'ingredientes': [],
                        'precio': 0,
                        'cantidad': cant,
                        'comentario': comentario,
                        'total': 0,
                    })
        
        # Imprimir para verificar
        return render(request, 'modificar_pedido2.html', {
            'pedidos_dict': detalles_items,
            'restaurante': restaurantes.nombre,
            'id': restaurantes.id,
        })
   
    elif request.method=="POST":
        # Obtener el item que estamos cambiando
        item = request.POST.get('item')
        comentario_nuevo = request.POST.get('comentario')
        cantidad_nueva = request.POST.get('cantidad')

        try:
            # Verificar si el item está en elegidos
            if item in elegidos:
                # Obtener el índice del item
                index = elegidos.index(item)
                
                # Actualizar el comentario y la cantidad
                request.session[f'2comentario_{item}'] = comentario_nuevo
                cantidad_list[index] = cantidad_nueva  # Actualiza la cantidad en la posición correspondiente

                # Almacenar en la sesión
                request.session['cantidad2'] = ",".join(cantidad_list)  # Guarda la lista actualizada
                
                return redirect('pedidos2', item=id)  # Redirige correctamente a la vista 'pedidos'
            else:
                raise ValueError("El item no está en la lista de elegidos.")

        except ValueError as ve:
            return render(request, 'modificar_pedido2.html', {
                'error': str(ve),
                'id': restaurantes.id,
            })
        except Exception as e:
            return render(request, 'modificar_pedido2.html', {
                'error': f"Ocurrió un error inesperado.{e}",
                'id': restaurantes.id,
            })    
def UbicacionView(request, id):
    id = int(id)
    restaurante = Restaurante.objects.filter(id=id).first()
    ubicacion = request.session.get("ubicacion", "")  # Valor por defecto vacío si no existe
    busqueda = request.session.get('busqueda')
    print("Busqueda ", busqueda)

    if ubicacion:
        ubicacion = ubicacion.split('+')

    # Inicializar variables
    reservacion = None
    p_d = None 

    if request.method == "GET":
        if restaurante:
            reservacion = Reservaciones_config.objects.filter(restaurante=restaurante.id).first()
            p_d = Pickup_Delivery.objects.filter(restaurante=restaurante.id).first()
        else:
            restaurante=None

        return render(request, 'ubicacion.html', {
            'delivery': p_d.active_delivery if p_d else False,
            'pickup': p_d.active_pickup if p_d else False,
            'reservaciones': reservacion.active if reservacion else False,
            'id': id,
            'latitud': ubicacion[0] if ubicacion else False,
            'longitud': ubicacion[1] if ubicacion else False,
            'ubicacion': ubicacion if ubicacion else False,
        })

    elif request.method == "POST":
        latitud = request.POST.get("latitude")
        longitud = request.POST.get("longitude")
        print("LATITUD: ", latitud, "LONGI ", longitud)

        if latitud and longitud:  # Validar que las coordenadas no estén vacías
            try:
                # Validar que latitud y longitud sean números
                latitud = float(latitud)
                longitud = float(longitud)

                request.session["ubicacion"] = f"{latitud}+{longitud}"  # Almacenar en la sesión
                busqueda = request.session.get('busqueda')

                if restaurante and id!=0:
                    reservacion = Reservaciones_config.objects.filter(restaurante=restaurante.id).first()
                    p_d = Pickup_Delivery.objects.filter(restaurante=restaurante.id).first()

                if busqueda and id == 0 :
                    print("FUNCIONA")
                    return redirect('resultados', texto=busqueda)

                elif request.session.get('registro') and id != 0 and restaurante:
                    url = reverse('registro_datos', kwargs={'id': id})
                    return redirect(url)

                elif p_d and p_d.active_delivery and id != 0 and restaurante:
                    return redirect('presentacion_one', item=restaurante.id)

                elif p_d and p_d.active_pickup and not p_d.active_delivery and id != 0 and restaurante:
                    return redirect('presentacion_three', item=restaurante.id)

                elif p_d and not p_d.active_delivery and not p_d.active_pickup and reservacion and reservacion.active and id != 0 and restaurante:
                    return redirect('presentacion_two', item=restaurante.id)
                else:
                    if id != 0:
                        return redirect('presentacion', item=restaurante.id)

            except ValueError as e:  # Captura errores de conversión de tipo
                return render(request, 'ubicacion.html', {
                    'error': f"Las coordenadas deben ser números válidos: {e}",
                    'ubicacion': ubicacion if ubicacion else False,
                })
            except Exception as e:  # Captura otras excepciones
                return render(request, 'ubicacion.html', {
                    'error': str(e),
                    'ubicacion': ubicacion if ubicacion else False,
                })
        else:
            return render(request, 'ubicacion.html', {
                'error': "Revise el formulario. Asegúrese de que las coordenadas no estén vacías.",
                'ubicacion': ubicacion if ubicacion else False,
            })
        
def EliminarPedidoView(request,key,id):
    if request.session.get("type") == True:  # true=pickup, false=delivery
        elegidos = request.session.get('elegidos2', 'No disponible')
        cantidad = request.session.get('cantidad2', 'No disponible')
        print('Elegidos 2 antes de eliminar: ', elegidos)
        print('Cantidad 2 antes de eliminar: ', cantidad)

        # Verificar si 'elegidos' tiene un solo elemento
        if ',' not in str(elegidos):
            elegidos = [elegidos]  # Convertir a lista con un solo elemento
        else:
            elegidos = elegidos.split(',')  # Dividir en lista

        # Hacer lo mismo para 'cantidad'
        if ',' not in str(cantidad):
            cantidad = [cantidad]  # Convertir a lista con un solo elemento
        else:
            cantidad = cantidad.split(',')  # Dividir en lista

        # Crear un diccionario para almacenar los detalles de los ítems
        detalles_items = {}

        # Iterar sobre los elegidos y sus cantidades
        for i in range(len(elegidos)):
            elegido = elegidos[i]
            cant = cantidad[i] if i < len(cantidad) else '0'  # Asegurarse de que la cantidad exista

            # Recuperar el comentario correspondiente
            comentario = request.session.get(f'2comentario_{elegido}', 'No disponible')

            detalles_items[i] = {
                'item': elegido,
                'cantidad': float(cant),  # Asegúrate de que sea float
            }

        key = int(key)  # Asegúrate de que 'key' sea un entero
        if key in detalles_items:
            detalles_items.pop(key)  # Eliminar el elemento correspondiente a 'key'

        # Actualizar la sesión con los elementos restantes
        nuevos_elegidos = []
        nuevos_cantidades = []

        for item in detalles_items.values():
            nuevos_elegidos.append(item['item'])
            nuevos_cantidades.append(str(item['cantidad']))
            del request.session[f'2comentario_{item["item"]}']  # Eliminar el comentario correspondiente

        # Guardar los nuevos valores en la sesión
        request.session['elegidos2'] = ','.join(nuevos_elegidos)  # Unir los elementos restantes
        request.session['cantidad2'] = ','.join(nuevos_cantidades)  # Unir las cantidades restantes

        elegidos = request.session.get('elegidos2', 'No disponible')
        cantidad = request.session.get('cantidad2', 'No disponible')
        print('Elegidos 2 luego de eliminar: ', elegidos)
        print('Cantidad 2 luego de eliminar: ', cantidad)

        return redirect("pedidos2", item=id)

    elif request.session.get("type")==False:

        elegidos = request.session.get('elegidos', 'No disponible')
        cantidad = request.session.get('cantidad', 'No disponible')

        print('Elegidos 1 anres de eliminar: ',elegidos)
        print ('Cantidad 1 antes de elminar: ',cantidad)

        # Verificar si 'elegidos' tiene un solo elemento
        if ',' not in str(elegidos):
            elegidos = [elegidos]  # Convertir a lista con un solo elemento
        else:
            elegidos = elegidos.split(',')  # Dividir en lista

        # Hacer lo mismo para 'cantidad'
        if ',' not in str(cantidad):
            cantidad = [cantidad]  # Convertir a lista con un solo elemento
        else:
            cantidad = cantidad.split(',')  # Dividir en lista

        # Crear un diccionario para almacenar los detalles de los ítems
        detalles_items = {}

        # Iterar sobre los elegidos y sus cantidades
        for i in range(len(elegidos)):
            elegido = elegidos[i]
            cant = cantidad[i] if i < len(cantidad) else '0'  # Asegurarse de que la cantidad exista

            # Recuperar el comentario correspondiente
            comentario = request.session.get(f'comentario_{elegido}', 'No disponible')

            detalles_items[i] = {
                'item': elegido,
                'cantidad': float(cant),  # Asegúrate de que sea float
            }
        
        if key in detalles_items:
            detalles_items.pop(key)
            for item in detalles_items.values():
                request.session['elegidos'] = ',' + item['item']
                request.session['cantidad'] = ',' + str(item['cantidad'])
                del request.session[f'comentario_{item["item"]}']
        elegidos = request.session.get('elegidos', 'No disponible')
        cantidad = request.session.get('cantidad', 'No disponible')
        print('Elegidos 1 luego de eliminar: ',elegidos)
        print ('Cantidad 1 luego de elminar: ',cantidad)
        return redirect("pedidos",item=id)
    
def UbicacionRestauranteView(request):
    id=request.session.get("restaurante")
    restaurante=Restaurante.objects.filter(id=id).first()
    restaurante.direccion=restaurante.direccion.split("+")
    direccion=obtener_direccion(restaurante.direccion[0],restaurante.direccion[1])
    return render(request,'ubicacion_restaurante.html',{
        'latitud': restaurante.direccion[0],
        'longitud':restaurante.direccion[1],
        'nombre': restaurante.nombre,
        'direccion':direccion,
    })
        
def obtener_ingredientes(codigo):
    #Función para obtener ingredientes a partir de los códigos.
    lista = codigo.split(',')
    ingredientes = []

    for codigo in lista:
        consulta = Ingredientes.objects.filter(codigo=codigo).values_list('ingrediente', flat=True)
        if consulta:
            ingredientes.append(consulta[0])
    return (ingredientes)

def obtener_direccion(param1,param2):
    param1=str(param1)
    param2=str(param2)
    geolocator = Nominatim(user_agent="MealMate")
    location = geolocator.reverse(f"{param1}, {param2}")
    return location.address

