from django.shortcuts import render,redirect
from django.urls import reverse
from django.core.paginator import Paginator
from user_r.models import Restaurante,Menu,Ingredientes,Pago,Paypal,Zelle
from servicios.models import Reservaciones_config,Pickup_Delivery
from .forms import BarraBusqueda,PedidoForm,UbicacionForm
from more_itertools import unique_everseen

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
        if form.is_valid():
            try:
                # Obtener el valor del campo del formulario
                search = form.cleaned_data['texto'].lower()
                resultados = []
                
                # Buscar coincidencias exactas en 'Menu'
                comidas = Menu.objects.filter(comida__icontains=search).values('comida', 'restaurante')
                if comidas.exists():
                    for comida in comidas:
                        restaurante = Restaurante.objects.filter(id=comida['restaurante']).first()
                        mail = request.session.get('email')
                        
                        # Si el restaurante no es del usuario, mostrar los resultados
                        if restaurante and restaurante.email != mail:
                            reservacion = Reservaciones_config.objects.filter(restaurante=restaurante.id).first()
                            pandd = Pickup_Delivery.objects.filter(restaurante=restaurante.id).first()

                            if restaurante:
                                resultados.append({
                                    'comida': comida['comida'],
                                    'restaurante_nombre': restaurante.nombre,
                                    'ubicacion': restaurante.direccion,
                                    'codigo': restaurante.id,
                                    'delivery': pandd.active_delivery if pandd else False,
                                    'pickup': pandd.active_pickup if pandd else False,
                                    'reservaciones': reservacion.active if reservacion else False
                                })

                else:    
                    # Buscar coincidencias en 'Ingredientes'
                    ingredientes = Menu.objects.all()
                    for ingredient in ingredientes:
                        lista = ingredient.codigo.split(',')
                        for codigo in lista:
                            # Buscar el código en la tabla ingredientes y sustituirlo por su palabra correspondiente
                            word = Ingredientes.objects.filter(codigo=codigo).first()
                            if word and search == word.ingrediente.lower():
                                # Si coincide con la barra de búsqueda
                                restaurante = Restaurante.objects.filter(id=ingredient.restaurante_id).first()
                                mail = request.session.get('email')
                                
                                # Si el restaurante no es del usuario, añadir a resultados
                                if restaurante and restaurante.email != mail:
                                    reservacion = Reservaciones_config.objects.filter(restaurante=restaurante.id).first()
                                    pandd = Pickup_Delivery.objects.filter(restaurante=restaurante.id).first()                                   
                                   
                                    resultados.append({
                                        'restaurante_nombre': restaurante.nombre,
                                        'ubicacion': restaurante.direccion,
                                        'codigo': restaurante.id,
                                        'delivery': pandd.active_delivery if pandd else False,
                                        'pickup': pandd.active_pickup if pandd else False,
                                        'reservaciones': reservacion.active if reservacion else False
                                    })

                # Eliminar duplicados usando unique_everseen 
                unique_resultados = list(unique_everseen(resultados))
                if not unique_resultados:
                    raise Exception("No se encontraron coincidencias")


                # Paginación
                paginator = Paginator(unique_resultados, 10)
                pagina = request.GET.get("page") or 1
                items = paginator.get_page(pagina)
                pagina_actual = int(pagina)
                paginas = range(1, items.paginator.num_pages + 1)

                return render(request, 'home.html', {
                    'busqueda': BarraBusqueda(),
                    'items': items,
                    'paginas': paginas,
                    'pagina_actual': pagina_actual,
                })
            except Exception as e:
                return render(request, 'home.html', {
                    'busqueda': BarraBusqueda(),
                    'error': f'{e}'
                })
        else:
            return render(request, 'home.html', {
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
    item = int(item)
    
    # Asegúrate de que 'restaurante' en la sesión sea un entero
    if request.session.get('restaurante'):
        request.session['restaurante'] = int(request.session['restaurante'])

    if request.method == 'GET':
        try:
            restaurante_sesion = request.session.get('restaurante')
            
            # Si el pedido que se estaba llenando no era del mismo restaurante, vaciar las variables de sesión
            if restaurante_sesion is not None and restaurante_sesion != item:
                # Guardar el valor de la variable que deseas conservar
                valor_a_conservar = request.session.get('email')

                # Vaciar todas las variables de sesión
                request.session.flush()

                # Restaurar la variable que deseas conservar
                request.session['email'] = valor_a_conservar

            if not request.session.get("ubicacion"):
                return redirect("ubicacion", id=item)
            else:
                restaurante = Restaurante.objects.get(id=item)
                reservacion = Reservaciones_config.objects.filter(restaurante=restaurante.id).first()
                pandd = Pickup_Delivery.objects.filter(restaurante=restaurante.id).first()  
                menu = Menu.objects.filter(restaurante=item)

                for menu_item in menu:
                    menu_item.codigo = obtener_ingredientes(menu_item.codigo)

                if request.session.get('elegidos')!="" and 'elegidos' in request.session:
                    activo=True
                else:
                    activo=False

                return render(request, 'delivery.html', {
                    'restaurante': restaurante, 
                    'menu': menu,
                    'ubicacion': request.session.get('ubicacion'),
                    'id': restaurante.id,
                    'form': PedidoForm(),
                    'delivery': pandd.active_delivery if pandd else False,
                    'pickup': pandd.active_pickup if pandd else False,
                    'reservaciones': reservacion.active if reservacion else False,
                    'activo': activo,
                })

        except Restaurante.DoesNotExist:
            return render(request, 'delivery.html', {
                'error': "El restaurante no se encontró.",
            })
        except Exception as e:
            return render(request, 'delivery.html', {
                'error': f"Que extraño, no hay coincidencias. Recargue la página por favor. Error: {e}",
                })

def PickupView(request, item):
    item=int(item)
    if request.session.get('restaurante'):
        request.session['restaurante'] = int(request.session['restaurante'])

    if request.method == 'GET':
        try:
            restaurante_sesion = request.session.get('restaurante')
            
            # Si el pedido que se estaba llenando no era del mismo restaurante, vaciar las variables de sesión
            if restaurante_sesion is not None and restaurante_sesion != item:
                # Guardar el valor de la variable que deseas conservar
                valor_a_conservar = request.session.get('email')

                # Vaciar todas las variables de sesión
                request.session.flush()

                # Restaurar la variable que deseas conservar
                request.session['email'] = valor_a_conservar

            # Obtener el restaurante y otros datos
            restaurante = Restaurante.objects.get(id=item)
            reservacion = Reservaciones_config.objects.filter(restaurante=restaurante.id).first()
            pandd = Pickup_Delivery.objects.filter(restaurante=restaurante.id).first()  
            menu = Menu.objects.filter(restaurante=item)

            for menu_item in menu:
                menu_item.codigo = obtener_ingredientes(menu_item.codigo)
            print("Elegidos 2: ",request.session.get('elegidos2'))
            if request.session.get('elegidos2')!="":
                activo=True
            else:
                activo=False

            return render(request, 'pickup.html', {
                'restaurante': restaurante, 
                'menu': menu,
                'id': restaurante.id,
                'delivery': pandd.active_delivery if pandd else False,
                'pickup': pandd.active_pickup if pandd else False,
                'reservaciones': reservacion.active if reservacion else False,
                'activo': activo,
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
        try:

            if request.session.get('restaurante')!=item:
                #vaciar las variables de sesion que arman los pedido cada que se entra a la pagina de inicio
                if 'cantidad' in request.session: 
                    del request.session['cantidad']
                if 'type' in request.session:
                    del request.session['type']

                if 'elegidos' in request.session:
                    for i in request.session['elegidos'].split(","):
                        if f'comentario_{i}' in request.session:
                            del request.session[f'comentario_{i}']
                    del request.session['elegidos']
                #pickup
                if 'cantidad2' in request.session: 
                    del request.session['cantidad2']

                if 'elegidos2' in request.session:
                    for i in request.session['elegidos2'].split(","):
                        if f'2comentario_{i}' in request.session:
                            del request.session[f'2comentario_{i}']
                    del request.session['2elegidos']
                #se borra la ubicacion ya que esto indica que el se coloco unaa ubicacion anteriror
                if 'ubicacion' in request.session: 
                        del request.session['ubicacion']
            
            if not request.session.get('ubicacion'):
                return redirect('ubicacion')
            else:
                restaurante = Restaurante.objects.filter(id=item).first()
                if not restaurante:
                    raise Restaurante.DoesNotExist
                
                reservacion = Reservaciones_config.objects.filter(restaurante=restaurante.id).first()
                pandd = Pickup_Delivery.objects.filter(restaurante=restaurante.id).first()  
                menu = Menu.objects.filter(restaurante=restaurante.id)
                
                for item in menu:
                    item.codigo = obtener_ingredientes(item.codigo) if item.codigo else []

                return render(request, 'reservaciones.html', {
                    'restaurante': restaurante,
                    'menu': menu,
                    'delivery': pandd.active_delivery if pandd else False,
                    'pickup': pandd.active_pickup if pandd else False,
                    'reservaciones': reservacion.active if reservacion else False
                })
        except Restaurante.DoesNotExist:
                return render(request, 'reservaciones.html', {
                    'error': "El restaurante no se encontró.",
                })
        except Exception as e:
                return render(request, 'reservaciones.html', {
                    'error': f"Que extraño, no hay coincidencias. Recargue la página por favor. Error: {e}"
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
                request.session['restaurante']=id
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
                detalles_items[i] = {
                    'item': elegido,
                    'comida': comida.comida,
                    'ingredientes': obtener_ingredientes(comida.codigo),
                    'precio': float(comida.precios),  # Asegúrate de que sea float
                    'cantidad': float(cant),  # Asegúrate de que sea float
                    'comentario': comentario,
                    'total': float(comida.precios) * float(cant),
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
                }

        # Calcular el total y el IVA
        total = sum(item['total'] for item in detalles_items.values())  # Sumar todos los totales
        iva = total + (total * 0.16)  # Total con IVA

        # Redondear los valores a dos decimales
        total = round(total, 2)
        iva = round(iva, 2)
        return render(request, 'pedidos.html', {
            'pedidos_dict': detalles_items,
            'restaurante': restaurante.nombre,
            'id': restaurante.id,
            'ubicacion':request.session.get("ubicacion"),
            'total': str(total),
            'iva': iva,
        })

def ModificarPedido(request, id, item):
    id=str(id)
    if request.method == "GET":
        restaurante = Restaurante.objects.filter(id=id).first()
        
        # Verificar si el restaurante existe
        if not restaurante:
            return render(request, 'modificar_pedido.html', {
                'error': 'Restaurante no encontrado',
            })

        # Recuperar las variables de sesión
        elegidos = request.session.get('elegidos', 'No disponible')
        cantidad = request.session.get('cantidad', '0')  # Cambiar a '0' por defecto

        # Convertir a listas
        if ',' not in str(elegidos):
            items = [elegidos]  # Convertir a lista con un solo elemento
        else:
            items = elegidos.nro_items.split(',')  # Dividir en lista
        
        if ',' not in str(cantidad):
            cantidad_list = [cantidad]  # Convertir a lista con un solo elemento
        else:
            cantidad_list = cantidad.split(',')  # Dividir en lista


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
        
        # Imprimir para verificar
        return render(request, 'modificar_pedido.html', {
            'pedidos_dict': detalles_items,
            'restaurante': restaurante.nombre,
            'item': restaurante.id,
        })
   
    elif request.method == "POST":
        # Obtener el item que estamos cambiando
        item = request.POST.get('item')
        comentario_nuevo = request.POST.get('comentario')
        cantidad_nueva = request.POST.get('cantidad')

        try:
            # Items elegidos
            if ',' not in request.session.get('elegidos', ''):
                elegidos_actual = [request.session.get('elegidos')]
            else:
                elegidos_actual = request.session.get('elegidos', '').split(',')

            if ',' not in request.session.get('cantidad', ''):
                cantidad_actual = [request.session.get('cantidad')]
            else:
                cantidad_actual = request.session.get('cantidad', '').split(',')
            
            # Verificar si el item está en elegidos
            if item in elegidos_actual:
                # Obtener el índice del item
                index = elegidos_actual.index(item)
                
                # Actualizar el comentario y la cantidad
                request.session[f'comentario_{item}'] = comentario_nuevo
                cantidad_actual[index] = cantidad_nueva  # Actualiza la cantidad en la posición correspondiente

                # Almacenar en la sesión
                request.session['cantidad'] = ",".join(cantidad_actual)  # Guarda la lista actualizada
                print("ID antes de redirigir:", id)
                item = str(id)
                return redirect('pedidos', item=item)  # Redirige correctamente a la vista 'pedidos'
            else:
                raise ValueError("El item no está en la lista de elegidos.")

        except ValueError as ve:
            return render(request, 'modificar_pedido.html', {
                'error': str(ve),
            })
        except Exception as e:
            return render(request, 'modificar_pedido.html', {
                'error': "Ocurrió un error inesperado.",
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
            comentario = request.session.get(f'2comentario_{elegido}', 'No disponible')

            if comida:  # Verificar que comida no sea None
                # Agregar los detalles a la lista
                detalles_items[i] = {
                    'item': elegido,
                    'comida': comida.comida,
                    'ingredientes': obtener_ingredientes(comida.codigo),
                    'precio': float(comida.precios),  # Asegúrate de que sea float
                    'cantidad': float(cant),  # Asegúrate de que sea float
                    'comentario': comentario,
                    'total': float(comida.precios) * float(cant),
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
                }

        # Calcular el total y el IVA
        
        total = sum(item['total'] for item in detalles_items.values())  # Sumar todos los totales
        iva = total + (total * 0.16)  # Total con IVA

        # Redondear los valores a dos decimales
        total = round(total, 2)
        iva = round(iva, 2)

        return render(request, 'pedidos2.html', {
            'pedidos_dict': detalles_items,
            'restaurante': restaurante.nombre,
            'id': restaurante.id,
            'total': total,
            'iva': iva,
        })

def ModificarPedido2(request, id, item):
    if request.method == "GET":
        restaurantes = Restaurante.objects.filter(id=id).first()
        
        # Verificar si el restaurante existe
        if not restaurantes:
            return render(request, 'modificar_pedido2.html', {
                'error': 'Restaurante no encontrado',
            })

        # Recuperar las variables de sesión
        elegidos = request.session.get('elegidos2', 'No disponible').split(',')
        cantidad = request.session.get('cantidad2', 'No disponible').split(',')

        # Crear una lista para almacenar los detalles de los ítems
        detalles_items = []

        # Iterar sobre los elegidos y sus cantidades
        for j, elegido in enumerate(elegidos):
            if elegido == item:  # Asegúrate de que 'item' esté definido en el contexto
                comida = Menu.objects.filter(item=elegido, restaurante=restaurantes.id).first()
                cant = cantidad[j] if j < len(cantidad) else '0'  # Asegurarse de que la cantidad exista

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
            # Items elegidos
            elegidos_actual = request.session.get('elegidos2', '').split(',')
            cantidad_actual = request.session.get('cantidad2', '').split(',')
            
            # Verificar si el item está en elegidos
            if item in elegidos_actual:
                # Obtener el índice del item
                index = elegidos_actual.index(item)
                
                # Actualizar el comentario y la cantidad
                request.session[f'2comentario_{item}'] = comentario_nuevo
                cantidad_actual[index] = cantidad_nueva  # Actualiza la cantidad en la posición correspondiente

                # Almacenar en la sesión
                request.session['cantidad2'] = ",".join(cantidad_actual)  # Guarda la lista actualizada
                
                return redirect('pedidos2', item=id)  # Redirige correctamente a la vista 'pedidos'
            else:
                raise ValueError("El item no está en la lista de elegidos.")

        except ValueError as ve:
            return render(request, 'modificar_pedido2.html', {
                'error': str(ve),
            })
        except Exception as e:
            return render(request, 'modificar_pedido2.html', {
                'error': "Ocurrió un error inesperado.",
            })    

def UbicacionView(request, id):
    restaurante = Restaurante.objects.filter(id=id).first()
    if request.method == "GET":
        ubicacion = request.session.get("ubicacion", "")  # Valor por defecto vacío si no existe
        form = UbicacionForm(initial={'ubicacion': ubicacion})  # Establecer el valor inicial
        reservacion = Reservaciones_config.objects.filter(restaurante=restaurante.id).first()
        pandd = Pickup_Delivery.objects.filter(restaurante=restaurante.id).first()

        return render(request, 'ubicacion.html', {
            'form': form,
            'delivery': pandd.active_delivery if pandd else False,
            'pickup': pandd.active_pickup if pandd else False,
            'reservaciones': reservacion.active if reservacion else False,
            'id':id,
            })
    
    elif request.method == "POST":
        form = UbicacionForm(request.POST)
        
        if form.is_valid():  # Validar el formulario
            try:
                request.session["ubicacion"] = form.cleaned_data['ubicacion']  # Acceder a cleaned_data

                reservacion = Reservaciones_config.objects.filter(restaurante=restaurante.id).first()
                p_d = Pickup_Delivery.objects.filter(restaurante=restaurante.id).first()
                
                if request.session.get('registro'):
                    url = reverse('registro_datos', kwargs={'id': id})
                    return redirect(url)
                
                if p_d.active_delivery: 
                    return redirect('presentacion_one', item=restaurante.id)
                elif p_d.active_pickup and not p_d.active_delivery:
                    return redirect('presentacion_three', item=restaurante.id)
                elif not p_d.active_delivery and not p_d.active_pickup and reservacion.active:
                    return redirect('presentacion_two', item=restaurante.id)
                else:
                    return redirect('presentacion', item=restaurante.id)
            
            except Exception as e:  # Cambia esto por una excepción específica
                return render(request, 'ubicacion.html', {'error': str(e), 'form': form})
        
        else:
            return render(request, 'ubicacion.html', {
                'error': "Revise el formulario",
                'form': form  # Mantener el formulario con los datos ingresados
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

        
def obtener_ingredientes(codigo):
    #Función para obtener ingredientes a partir de los códigos.
    lista = codigo.split(',')
    ingredientes = []

    for codigo in lista:
        consulta = Ingredientes.objects.filter(codigo=codigo).values_list('ingrediente', flat=True)
        if consulta:
            ingredientes.append(consulta[0])
    return (ingredientes)