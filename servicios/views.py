from django.shortcuts import render,redirect
from .models import Reservaciones_config,Pickup_Delivery,Reservaciones_horario
from .forms import CheckPickForm,CheckReserForm,CheckDelivForm
from usuario_sesion.forms import IniciarSesion
from user_r.models import Restaurante
from pedidos.models import PedidoModel
from datetime import date,datetime
from pedidos.models import PedidoModel
from django.http import JsonResponse
from django.utils import timezone
import datetime

# Create your views here.

def ActivateReserView(request):
    #obtencion de la variable de sesion email
    mail = request.session.get('email')
    if not mail:
        return render(request, 'usuario_sesion/login.html', {
            'form': IniciarSesion(),
            'error': 'Email o contraseña incorrecto'
        })
    
    
    elif mail and request.method == 'GET':
        restaurante=Restaurante.objects.filter(email=mail).first()
        if restaurante and restaurante.is_active:
            # Busca una instancia existente de REservaciones o crea una nueva si no existe
            r_instance = Reservaciones_config.objects.filter(restaurante=restaurante.id).first()           
            if not r_instance:
                    r_instance = Reservaciones_config(restaurante=restaurante)
            if r_instance.active:
                return redirect('mesas')
            form = CheckReserForm(instance=r_instance)

            return render(request, 'activate_r.html', {'form': form, 'nombre': restaurante.nombre,})

    elif mail and request.method == 'POST':
        restaurante=Restaurante.objects.filter(email=mail).first()
        if restaurante and restaurante.is_active:

            r_instance = Reservaciones_config.objects.filter(restaurante=restaurante).first()

            if not r_instance:
                    r_instance = Reservaciones_config(restaurante=restaurante)

            form = CheckReserForm(request.POST, instance=r_instance)
            if form.is_valid():
                try:
                    form.save()  # Guarda la instancia con el cambio realizado
                    return redirect('activate_r')
                except ValueError:
                    return render(request, 'activate_r.html', {
                            'form': form,
                            'nombre': restaurante.nombre,
                            'error': 'Error actualizando datos'
                    })
            else:
                return render(request, 'activate_r.html', {
                        'form': form,
                        'nombre': restaurante.nombre,
                        'error': 'Por favor, corrige los errores en el formulario.'
                })

def ActivateDelivView(request):
    #obtencion de la variable de sesion email
    mail = request.session.get('email')
    if not mail:
        return render(request, 'usuario_sesion/login.html', {
            'form': IniciarSesion(),
            'error': 'Email o contraseña incorrecto'
        })
    
    
    elif mail and request.method == 'GET':
        restaurante=Restaurante.objects.filter(email=mail).first()
        if restaurante and restaurante.is_active:
            # Busca una instancia existente de REservaciones o crea una nueva si no existe
            d_instance = Pickup_Delivery.objects.filter(restaurante=restaurante.id).first()
            if not d_instance:
                d_instance = Pickup_Delivery(restaurante=restaurante)
            if(d_instance.active_delivery):
                return redirect('delivery')
            form = CheckDelivForm(instance=d_instance)

            return render(request, 'activate_d.html', {'form': form, 'nombre': restaurante.nombre,})

    elif mail and request.method == 'POST':
        restaurante=Restaurante.objects.filter(email=mail).first()
        if restaurante and restaurante.is_active:

            d_instance = Pickup_Delivery.objects.filter(restaurante=restaurante).first()

            if not d_instance:
                d_instance = Pickup_Delivery(restaurante=restaurante)

            form = CheckDelivForm(request.POST, instance=d_instance)
            if form.is_valid():
                try:
                    form.save()  # Guarda la instancia con el cambio realizado
                    return redirect('activate_d')
                except ValueError:
                    return render(request, 'activate_d.html', {
                            'form': form,
                            'nombre': restaurante.nombre,
                            'error': 'Error actualizando datos'
                    })
            else:
                return render(request, 'activate_d.html', {
                        'form': form,
                        'nombre': restaurante.nombre,
                        'error': 'Por favor, corrige los errores en el formulario.'
                })

def ActivatePickView(request):
    #obtencion de la variable de sesion email
    mail = request.session.get('email')
    if not mail:
        return render(request, 'usuario_sesion/login.html', {
            'form': IniciarSesion(),
            'error': 'Email o contraseña incorrecto'
        })
    
    
    elif mail and request.method == 'GET':
        restaurante=Restaurante.objects.filter(email=mail).first()
        if restaurante and restaurante.is_active:
            # Busca una instancia existente de REservaciones o crea una nueva si no existe
            p_instance = Pickup_Delivery.objects.filter(restaurante=restaurante.id).first()
            if not p_instance:
                p_instance = Pickup_Delivery(restaurante=restaurante)
            if(p_instance.active_pickup):
                return redirect('pickup')
            form = CheckPickForm(instance=p_instance)

            return render(request,'activate_p.html', {'form': form, 'nombre': restaurante.nombre,})

    elif mail and request.method == 'POST':
        restaurante=Restaurante.objects.filter(email=mail).first()
        if restaurante and restaurante.is_active:

            p_instance = Pickup_Delivery.objects.filter(restaurante=restaurante).first()

            if not p_instance:
                p_instance = Pickup_Delivery(restaurante=restaurante)

            form = CheckPickForm(request.POST, instance=p_instance)
            if form.is_valid():
                try:
                    form.save()  # Guarda la instancia con el cambio realizado
                    return redirect('activate_p')
                except ValueError:
                    return render(request, 'activate_p.html', {
                            'form': form,
                            'nombre': restaurante.nombre,
                            'error': 'Error actualizando datos'
                    })
            else:
                return render(request, 'activate_p.html', {
                        'form': form,
                        'nombre': restaurante.nombre,
                        'error': 'Por favor, corrige los errores en el formulario.'
                })
  #pedidos y horario de trabajo          
def DeliveryView(request):
    # Obtención de la variable de sesión email
    mail = request.session.get('email')
    
    if not mail:
        return render(request, 'usuario_sesion/login.html', {
            'form': IniciarSesion(),
            'error': 'Email o contraseña incorrecto'
        })

    restaurante = Restaurante.objects.filter(email=mail).first()
    if not restaurante:
        return render(request, 'usuario_sesion/login.html', {
            'form': IniciarSesion(),
            'error': 'Restaurante no encontrado'
        })

    delivery = Pickup_Delivery.objects.filter(restaurante=restaurante.id).first()
    if delivery and delivery.active_delivery:
        if request.method == 'GET':
            # Obtener los pedidos del restaurante
            pedidos = PedidoModel.objects.filter(id_nro=restaurante.id,is_pickup=False,is_delivery=True).all()

            # Obtener la fecha actual
            fecha_actual = timezone.now()

            for pedido in pedidos:
                # Verificar si la fecha del pedido es más antigua que un día
                if pedido.fecha < fecha_actual - datetime.timedelta(days=1):
                    pedido.delete()  # Eliminar el pedido de la base de datos
            check = CheckDelivForm(initial={
                'active_delivery': delivery.active_delivery,
            })

            # Formatear los tiempos para el input de tipo time
            inicio = delivery.d_start_time.strftime('%H:%M') if delivery.d_start_time else ''
            cierre = delivery.d_end_time.strftime('%H:%M') if delivery.d_end_time else ''

            return render(request, 'servicios/delivery.html', {
                'check': check,
                'inicio':inicio,
                'cierre': cierre,
                'pedidos':pedidos,
                'nombre': restaurante.nombre,
            })

        elif request.method == 'POST':
            check = CheckDelivForm(request.POST, instance=delivery)  # Inicializa check aquí

            #horario de trabajo del delivery
            inicio = request.POST.get('inicio')  # Captura el valor de inicio
            cierre = request.POST.get('cierre')  # Captura el valor de cierre
            #status del pedido: true=entregado o false=sin entrgar
            status = request.POST.get('status')
            nro = request.POST.get('nro')

            try:
                if inicio and cierre:
                # guardar en el modelo
                    delivery.d_start_time = inicio
                    delivery.d_end_time = cierre
                    delivery.save()

                if status and nro:
                    if delivery.active_delivery==True:
                        delivery.active_pickup=True
                        delivery.save()
                    pedido=PedidoModel.objects.filter(nro=nro,id_nro=restaurante.id,is_pickup=False,is_delivery=True).first()
                    pedido.status=status
                    pedido.save()

                # Solo guarda check si es válido
                if check.is_valid():
                    # Aquí puedes decidir si quieres actualizar el estado del delivery
                    check.save()  # Guarda el formulario check

                return redirect('delivery')

            except Exception as e:
                # Si hay un error, renderiza la plantilla con los formularios
                return render(request, 'servicios/delivery.html', {
                    'check': check,  # Muestra el formulario check con los datos actuales
                    'error': f'Error al guardar los cambios: {str(e)}',
                })
    else:
        return redirect('activate_d')

    # Este render puede ser innecesario si ya has manejado todos los casos
    return render(request, 'servicios/delivery.html', {
        'check': CheckDelivForm(initial={'active_delivery': delivery.active_delivery}),
    })

def PickupView(request):
    # Obtención de la variable de sesión email
    mail = request.session.get('email')
    
    if not mail:
        return render(request, 'usuario_sesion/login.html', {
            'form': IniciarSesion(),
            'error': 'Email o contraseña incorrecto'
        })

    restaurante = Restaurante.objects.filter(email=mail).first()
    if not restaurante:
        return render(request, 'usuario_sesion/login.html', {
            'form': IniciarSesion(),
            'error': 'Restaurante no encontrado'
        })

    pickup = Pickup_Delivery.objects.filter(restaurante=restaurante.id).first()
    
    if pickup and pickup.active_pickup:
        if request.method == 'GET':
            # Obtener los pedidos del restaurante
            pedidos = PedidoModel.objects.filter(id_nro=restaurante.id,is_pickup=True,is_delivery=False).all()

            # Obtener la fecha actual
            fecha_actual = timezone.now()

            for pedido in pedidos:
                # Verificar si la fecha del pedido es más antigua que un día
                if pedido.fecha < fecha_actual - datetime.timedelta(days=1):
                    pedido.delete()  # Eliminar el pedido de la base de datos
            check = CheckPickForm(initial={
                'active_pickup': pickup.active_pickup,
            })

            # Formatear los tiempos para el input de tipo time
            inicio = pickup.p_start_time.strftime('%H:%M') if pickup.p_start_time else ''
            cierre = pickup.p_end_time.strftime('%H:%M') if pickup.p_end_time else ''

            return render(request, 'pickup_servicios.html', {
                'check': check,
                'inicio':inicio,
                'cierre': cierre,
                'pedidos':pedidos,
                'nombre': restaurante.nombre,
            })

        elif request.method == 'POST':
            check = CheckPickForm(request.POST, instance=pickup)  # Inicializa check aquí
            inicio = request.POST.get('inicio')  # Captura el valor de inicio
            cierre = request.POST.get('cierre')  # Captura el valor de cierre
            status = request.POST.get('status')
            nro = request.POST.get('nro')
            try:
                if inicio and cierre:
                # guardar en el modelo
                    pickup.p_start_time = inicio
                    pickup.p_end_time = cierre
                    pickup.save()
                if status and nro:
                    if pickup.active_pickup==True:
                        pickup.active_pickup=True
                        pickup.save()
                    pedido=PedidoModel.objects.filter(nro=nro,id_nro=restaurante.id,is_pickup=True,is_delivery=False).first()
                    pedido.status=status
                    pedido.save()
                # Solo guarda check si es válido
                if check.is_valid():
                    # Aquí puedes decidir si quieres actualizar el estado del pickup
                    check.save()  # Guarda el formulario check

                return redirect('pickup')

            except Exception as e:
                # Si hay un error, renderiza la plantilla con los formularios
                return render(request, 'pickup_servicios.html', {
                    'check': check,  # Muestra el formulario check con los datos actuales
                    'error': f'Error al guardar los cambios: {str(e)}',
                })
    else:
        return redirect('activate_p')

    # Este render puede ser innecesario si ya has manejado todos los casos
    return render(request, 'pickup_servicios.html', {
        'check': CheckPickForm(initial={'active_pickup':pickup.active_pickup}),
    })


def MesasView(request):
    # Obtención de la variable de sesión email
    mail = request.session.get('email')
    
    if not mail:
        return render(request, 'usuario_sesion/login.html', {
            'form': IniciarSesion(),
            'error': 'Email o contraseña incorrecto'
        })

    restaurante = Restaurante.objects.filter(email=mail).first()
    if not restaurante:
        return render(request, 'usuario_sesion/login.html', {
            'form': IniciarSesion(),
            'error': 'Restaurante no encontrado'
        })

    reservacion = Reservaciones_config.objects.filter(restaurante=restaurante.id).first()
    if reservacion and reservacion.mesas:
        mesas = reservacion.mesas.split(',')
    else:
        mesas = []

    if reservacion and reservacion.active:
        if request.method == 'GET':
            check = CheckReserForm(initial={
                'active': reservacion.active,
            })

            return render(request, 'mesas.html', {
                'check': check,
                'mesas':mesas,
                'nombre': restaurante.nombre,
            })

        elif request.method == 'POST':
            check = CheckReserForm(request.POST, instance=reservacion)
            puestos = request.POST.getlist('puestos') 
            try:
                
                if puestos:
                    cadena = ','.join(puestos)
                    reservacion.mesas=cadena
                    reservacion.save()

                # Solo guarda check si es válido
                if check.is_valid():
                    # Aquí puedes decidir si quieres actualizar el estado del pickup
                    check.save()  # Guarda el formulario check

                return redirect('mesas')

            except Exception as e:
                # Si hay un error, renderiza la plantilla con los formularios
                return render(request, 'mesas.html', {
                    'check': check,  # Muestra el formulario check con los datos actuales
                    'error': f'Error al guardar los cambios: {str(e)}',
                    'mesas':mesas,
                })
    else:
        return redirect('activate_r')

def HorariosMesasViews(request):
    # Obtención de la variable de sesión email
    mail = request.session.get('email')
    
    if not mail:
        return render(request, 'usuario_sesion/login.html', {
            'form': IniciarSesion(),
            'error': 'Email o contraseña incorrecto'
        })

    restaurante = Restaurante.objects.filter(email=mail).first()
    if not restaurante:
        return render(request, 'usuario_sesion/login.html', {
            'form': IniciarSesion(),
            'error': 'Restaurante no encontrado'
        })

    reservacion = Reservaciones_config.objects.filter(restaurante=restaurante.id).first()
    
    if reservacion and reservacion.active:
        if request.method == 'GET':
            check = CheckReserForm(initial={
                'active': reservacion.active,
            })

            instance = Reservaciones_horario.objects.filter(restaurante=restaurante.id)

            if not instance.exists():
                instance = Reservaciones_horario(restaurante=restaurante)
                horarios = []
            else:           
                horarios = {}
                for reservacion in instance:
                    fecha = reservacion.fecha.strftime('%Y-%m-%d')
                    if fecha not in horarios:
                        horarios[fecha] = []
                    horarios[fecha].append({
                        'mesa': reservacion.mesa,
                        'horas': reservacion.horas.split(','),
                        'fecha_str': str(fecha)
                    })  
                    
            return render(request, 'horarios_mesas.html', {
                'check': check,
                'horarios': horarios,
                'nombre': restaurante.nombre,
            })

        elif request.method == 'POST':
            check = CheckReserForm(request.POST or None, instance=reservacion)  # Inicializa check aquí
            
            try:
                fecha = request.POST.get('fecha')
                mesa = request.POST.get('mesa')
                if fecha and mesa:
                    instance = Reservaciones_horario.objects.filter(
                        restaurante=restaurante.id,
                        fecha=fecha,
                        mesa=mesa
                    )
                    if instance.exists():
                        instance.delete()
                        print(f"Reservación para la fecha {fecha} y mesa {mesa} ha sido eliminada.")
                    else:
                        print("No se encontró ninguna reservación para eliminar.")
                if check.is_valid():  # Valida el formulario antes de guardar
                    check.save()  # Guarda el formulario check
                    return redirect('horarios_mesas')
            except Exception as e:
                    return render(request, 'horarios_mesas.html', {
                        'error': f'Error al guardar los cambios: {str(e)}',
                    })
    else:
        return redirect('activate_r')  


def HorarioNew(request):
    mail = request.session.get('email')
    
    if not mail:
        return render(request, 'usuario_sesion/login.html', {
            'form': IniciarSesion(),
            'error': 'Email o contraseña incorrecto'
        })

    restaurante = Restaurante.objects.filter(email=mail).first()
    if not restaurante:
        return render(request, 'usuario_sesion/login.html', {
            'form': IniciarSesion(),
            'error': 'Restaurante no encontrado'
        })

    reservacion = Reservaciones_config.objects.filter(restaurante=restaurante.id).first()
    
    if reservacion and reservacion.active:
        if request.method == 'GET':
            mesas = reservacion.mesas.split(',') 
            mesas_count = len(mesas) 
            mesas_range = list(range(mesas_count))
            fecha_actual = date.today()
            mes_siguiente = fecha_actual.month % 12 + 1
            year_siguiente = fecha_actual.year + (fecha_actual.month // 12)
            fecha_mas_un_mes = date(year_siguiente, mes_siguiente, fecha_actual.day)
            return render(request, 'new_horario.html', {
                'mesas': mesas_range,
                'hoy': fecha_actual.strftime('%Y-%m-%d'),
                'mes': fecha_mas_un_mes.strftime('%Y-%m-%d')
            })
        
        elif request.method == "POST":
            fecha = request.POST.get('fecha')
            mesa = request.POST.get('mesa')
            hora = request.POST.get('hora')

            if fecha and mesa and hora:
                try:
                    instance = Reservaciones_horario.objects.filter(
                        restaurante=restaurante.id,
                        fecha=fecha,
                        mesa=mesa
                    ).first()

                    if instance:
                        horas_existentes = instance.horas.split(",") if instance.horas else []
                        if hora not in horas_existentes:
                            horas_existentes.append(hora)
                            instance.horas = ",".join(horas_existentes)
                            instance.save()
                    else:
                        instance2 = Reservaciones_horario(
                            restaurante=restaurante,
                            fecha=fecha,
                            horas=hora,
                            mesa=mesa,
                        )

                        instance2.save()
                    
                    # Devuelve una respuesta JSON indicando éxito
                    return JsonResponse({'success': True, 'redirect_url': 'horarios_mesas'})
                except Exception as e:
                    return JsonResponse({'success': False, 'error': f'Error al guardar los cambios: {str(e)}'})
            else:
                return JsonResponse({'success': False, 'error': 'Todos los campos son obligatorios.'})
    else:
        return redirect("activate_r")

    return redirect("activate_r")

def ModificarReserva(request, param1, param2, param3): 
    mail = request.session.get('email')
    
    if not mail:
        return render(request, 'usuario_sesion/login.html', {
            'form': IniciarSesion(),
            'error': 'Email o contraseña incorrecto'
        })

    restaurante = Restaurante.objects.filter(email=mail).first()
    if not restaurante:
        return render(request, 'usuario_sesion/login.html', {
            'form': IniciarSesion(),
            'error': 'Restaurante no encontrado'
        })

    reservacion = Reservaciones_config.objects.filter(restaurante=restaurante.id).first()
    
    if reservacion and reservacion.active:
        if request.method == 'GET':
            mesas = reservacion.mesas.split(',') 
            mesas_count = len(mesas)
            mesas_range = list(range(mesas_count))
            fecha_actual = date.today()
            mes_siguiente = fecha_actual.month % 12 + 1
            year_siguiente = fecha_actual.year + (fecha_actual.month // 12)
            fecha_mas_un_mes = date(year_siguiente, mes_siguiente, fecha_actual.day)
            fecha_str = param1 
            fecha_obj = datetime.strptime(fecha_str, '%Y-%m-%d') 
            return render(request, 'modificar_reserva.html', {
                'mesas': mesas_range,
                'hoy': fecha_actual.strftime('%Y-%m-%d'),
                'mes': fecha_mas_un_mes.strftime('%Y-%m-%d'),
                'fecha': fecha_obj.strftime('%Y-%m-%d'),
                'mesa': int(param2) ,  # Asegúrate de que param2 sea un número
                'hora': param3,
            })
        
        elif request.method == "POST":
            fecha = request.POST.get('fecha')
            mesa = request.POST.get('mesa')
            hora = request.POST.get('hora')
            if fecha and mesa and hora:
                try:
                    instance = Reservaciones_horario.objects.filter(
                        restaurante=restaurante.id,
                        fecha=fecha,
                        mesa=mesa
                    ).first()

                    if instance:
                        horas_existentes = instance.horas.split(",") if instance.horas else []
                        if hora not in horas_existentes:
                            horas_existentes.append(hora)
                            instance.horas = ",".join(horas_existentes)
                            instance.save()
                    else:
                        instance2 = Reservaciones_horario(
                            restaurante=restaurante,
                            fecha=fecha,
                            horas=hora,
                            mesa=mesa,
                        )
                        instance2.save()
                    
                    # Redirigir a la página de horarios
                    return redirect('horarios_mesas')
                except Exception as e:
                    fecha_actual = date.today()
                    mes_siguiente = fecha_actual.month % 12 + 1
                    year_siguiente = fecha_actual.year + (fecha_actual.month // 12)
                    fecha_mas_un_mes = date(year_siguiente, mes_siguiente, fecha_actual.day)
                    fecha_str = param1 
                    fecha_obj = datetime.strptime(fecha_str, '%Y-%m-%d') 
                    return render(request, 'modificar_reserva.html', {
                        'error': f'Error al guardar los cambios: {str(e)}',
                        'fecha': fecha,
                        'mesa': mesa,
                        'hora': hora,
                    })
            else:
                fecha_actual = date.today()
                mes_siguiente = fecha_actual.month % 12 + 1
                year_siguiente = fecha_actual.year + (fecha_actual.month // 12)
                fecha_mas_un_mes = date(year_siguiente, mes_siguiente, fecha_actual.day)
                fecha_str = param1 
                fecha_obj = datetime.strptime(fecha_str, '%Y-%m-%d') 
                return render(request, 'modificar_reserva.html', {
                    'error': 'Todos los campos son obligatorios.',
                    'fecha': fecha,
                    'mesa': mesa,
                    'hora': hora,
                })
    else:
        return redirect("activate_r")

    return redirect("activate_r")