from django.shortcuts import render,redirect
from .models import PedidoModel,ZelleModel,PagoMovil,PaypalModel,PagoEfectivo
from user_r.models import Restaurante,Menu,Ingredientes,Pago,Paypal,Zelle
from servicios.models import Reservaciones_config,Reservaciones_horario,Pickup_Delivery,Reservacion_cliente
from usuario_sesion.models import Cliente
from usuario_sesion.forms import IniciarSesion
from .forms import Datos_Form,PagoMovilForm,PagoPaypalForm,PagoZelleForm,EfectivoForm
from django.utils import timezone
from datetime import datetime
import csv
import requests
from geopy.geocoders import Nominatim

# Create your views here.

def read_banks(value):
    banks = []
    try:
        with open('D:/Uni/lenguaje_programacion_1/proyecto/banks_venezuela.csv', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                banks.append((row[0], row[1]))  # Devuelve tuplas (value, display)
    except FileNotFoundError:
        print("El archivo CSV no se encontró en la ruta especificada.")
    except Exception as e:
        print(f"Ocurrió un error al leer el archivo CSV: {e}")

    for bank in banks:
        if bank[0] == value:
            return bank[1]
    return None  # Si no se encuentra el valor, retorna None

def DetailsDelivery(request,nro):
    mail = request.session.get('email')
    if not mail:
        return render(request, 'usuario_sesion/login.html', {
            'form': IniciarSesion(),
            'error': 'Email o contraseña incorrecto'
        })
    else:
        restaurante=Restaurante.objects.filter(email=mail).first()
        if request.method=="GET":
            
            #nro inidca el pedido en la base de datos, cada uno tiene un numero diferente
            pedido=PedidoModel.objects.filter(id_nro=restaurante.id,nro=nro,is_delivery=True,is_pickup=False).first()

            # Verificar si 'elegidos' tiene un solo elemento
            if ',' not in str(pedido.nro_items):
                items = [pedido.nro_items]  # Convertir a lista con un solo elemento
            else:
                items = pedido.nro_items.split(',')  # Dividir en lista

            # Hacer lo mismo para 'cantidad'
            if ',' not in str(pedido.cantidades):
                cantidad = [pedido.cantidades]  # Convertir a lista con un solo elemento
            else:
                cantidad = pedido.cantidades.split(',')  # Dividir en lista

            # Crear un diccionario para almacenar los detalles de los ítems
            detalles_items = {}
            #comentarioo={[Sin..];[Sin..]:}
            comentario=pedido.notas.split(';')
            # Iterar sobre los elegidos y sus cantidades
            for i in range(len(items)):
                elegido = items[i]
                #obtener el nombre de la comida segun su codigo
                comida = Menu.objects.filter(item=elegido, restaurante=restaurante.id).first()
                #obtener la cantiddad que se pidio de esa comida
                cant = cantidad[i] if i < len(cantidad) else '0'  # Asegurarse de que la cantidad exista

                comentario = comentario[i] if i < len(comentario) else '0'  # Asegurarse de que la cantidad exista

                if comida:  # Verificar que comida no sea None
                    # Agregar los detalles a la lista
                    #i es la comida pedida 1
                    detalles_items[i] = {
                        'item': elegido,
                        'comida': comida.comida,
                        'ingredientes': obtener_ingredientes(comida.codigo),
                        'cantidad': float(cant),  # Asegúrate de que sea float
                        'comentario': comentario,
                        'precio': float(comida.precios) * float(cant),
                        'bolivar':cambio_dolar(float(comida.precios) * float(cant)),
                    }
                else:
                    # Manejar el caso donde no se encuentra la comida
                    detalles_items[i] = {
                        'item': elegido,
                        'comida': 'No disponible',
                        'ingredientes': [],
                        'cantidad': float(cant),  # Asegúrate de que sea float
                        'comentario': comentario,
                        'precio':0,
                        'bolivar':0,
                    }

            total = sum(item['precio'] for item in detalles_items.values())  # Sumar todos los totales
            iva = total + (total * 0.16)  # Total con IVA
            bolivares=cambio_dolar(iva)
            bolivares=float(bolivares)
            #pago,nro=nro de pedido

            pago_nacional=PagoMovil.objects.filter(pedido=nro).first()
            zelle=ZelleModel.objects.filter(pedido=nro).first()
            paypal=PaypalModel.objects.filter(pedido=nro).first()
            efectivo=PagoEfectivo.objects.filter(pedido=nro).first()

            diccionario=False

            if pago_nacional:
                pago=pago_nacional
                pago.banco = read_banks(pago.banco)
                text="Pago Movil"
            elif zelle:
                pago=zelle
                text="Zelle"
            elif paypal:
                pago=paypal
                text="Paypal"
            elif efectivo:
                text = "Efectivo"
                efectivo.billetes = efectivo.billetes.split(',')
                name = ['1$', '5$', '10$', '20$', '50$', '100$']
                pago = {}

                for i in range(len(efectivo.billetes)):  # Usa range para iterar sobre los índices
                    cantidad = int(efectivo.billetes[i])  # Convierte a entero
                    if cantidad != 0:  # Verifica si la cantidad no es cero
                        pago[name[i]] = cantidad  # Asigna la cantidad al nombre correspondiente

                diccionario = True

            return render(request, 'detail_pickup.html',{
                'pedidos':pedido,
                'nombre':restaurante.nombre,
                'detalles':detalles_items,
                'subtotal': round(total, 2),
                'iva': round(iva, 2),
                'bolivares': round(bolivares,2),
                'pago':pago,
                'text':text,
                'diccionario': diccionario,
            })
        else:#request("POST")
            status = request.POST.get('status')
            try:

                if status and nro:
                    pedido=PedidoModel.objects.filter(id_nro=restaurante.id,nro=nro,is_pickup=False,is_delivery=True).first()
                    pedido.status=status
                    pedido.save()

                return redirect('detail_delivery',nro=nro)
            except Exception as e:
                # Si hay un error, renderiza la plantilla con los formularios
                return render(request, 'detail_delivery.html', {
                      # Muestra el formulario check con los datos actuales
                    'error': f'Error al guardar los cambios: {str(e)}',
                })
            
def DetailsPickup(request,nro):
    mail = request.session.get('email')
    if not mail:
        return render(request, 'usuario_sesion/login.html', {
            'form': IniciarSesion(),
            'error': 'Email o contraseña incorrecto'
        })
    else:
        restaurante=Restaurante.objects.filter(email=mail).first()
        if request.method=="GET":
            
            #nro inidca el pedido en la base de datos, cada uno tiene un numero diferente
            pedido=PedidoModel.objects.filter(id_nro=restaurante.id,nro=nro,is_pickup=True,is_delivery=False).first()

            # Verificar si 'elegidos' tiene un solo elemento
            if ',' not in str(pedido.nro_items):
                items = [pedido.nro_items]  # Convertir a lista con un solo elemento
            else:
                items = pedido.nro_items.split(',')  # Dividir en lista

            # Hacer lo mismo para 'cantidad'
            if ',' not in str(pedido.cantidades):
                cantidad = [pedido.cantidades]  # Convertir a lista con un solo elemento
            else:
                cantidad = pedido.cantidades.split(',')  # Dividir en lista

            # Crear un diccionario para almacenar los detalles de los ítems
            detalles_items = {}
            #comentarioo={[Sin..];[Sin..]:}
            comentario=pedido.notas.split(';')
            # Iterar sobre los elegidos y sus cantidades
            for i in range(len(items)):
                elegido = items[i]
                #obtener el nombre de la comida segun su codigo
                comida = Menu.objects.filter(item=elegido, restaurante=restaurante.id).first()
                #obtener la cantiddad que se pidio de esa comida
                cant = cantidad[i] if i < len(cantidad) else '0'  # Asegurarse de que la cantidad exista

                comentario = comentario[i] if i < len(comentario) else '0'  # Asegurarse de que la cantidad exista

                if comida:  # Verificar que comida no sea None
                    # Agregar los detalles a la lista
                    #i es la comida pedida 1
                    bolivar=cambio_dolar(float(comida.precios) * float(cant))
                    bolivar=float(bolivar)
                    bolivar=round(bolivar,2)
                    detalles_items[i] = {
                        'item': elegido,
                        'comida': comida.comida,
                        'ingredientes': obtener_ingredientes(comida.codigo),
                        'cantidad': float(cant),  # Asegúrate de que sea float
                        'comentario': comentario,
                        'precio': float(comida.precios) * float(cant),
                        'bolivar':bolivar,
                    }
                else:
                    # Manejar el caso donde no se encuentra la comida
                    detalles_items[i] = {
                        'item': elegido,
                        'comida': 'No disponible',
                        'ingredientes': [],
                        'cantidad': float(cant),  # Asegúrate de que sea float
                        'comentario': comentario,
                        'precio':0,
                        'bolivar':0,
                    }

            total = sum(item['precio'] for item in detalles_items.values())  # Sumar todos los totales
            iva = total + (total * 0.16)  # Total con IVA
            bolivares=cambio_dolar(iva)
            bolivares=float(bolivares)
            #pago,nro=nro de pedido

            pago_nacional=PagoMovil.objects.filter(pedido=nro).first()
            zelle=ZelleModel.objects.filter(pedido=nro).first()
            paypal=PaypalModel.objects.filter(pedido=nro).first()
            efectivo=PagoEfectivo.objects.filter(pedido=nro).first()

            diccionario=False

            if pago_nacional:
                pago=pago_nacional
                pago.banco = read_banks(pago.banco)
                text="Pago Movil"
            elif zelle:
                pago=zelle
                text="Zelle"
            elif paypal:
                pago=paypal
                text="Paypal"
            elif efectivo:
                text = "Efectivo"
                efectivo.billetes = efectivo.billetes.split(',')
                name = ['1$', '5$', '10$', '20$', '50$', '100$']
                pago = {}

                for i in range(len(efectivo.billetes)):  # Usa range para iterar sobre los índices
                    cantidad = int(efectivo.billetes[i])  # Convierte a entero
                    if cantidad != 0:  # Verifica si la cantidad no es cero
                        pago[name[i]] = cantidad  # Asigna la cantidad al nombre correspondiente

                diccionario = True

            return render(request, 'detail_pickup.html',{
                'pedidos':pedido,
                'nombre':restaurante.nombre,
                'detalles':detalles_items,
                'subtotal': round(total, 2),
                'iva': round(iva, 2),
                'bolivares': round(bolivares,2),
                'pago':pago,
                'text':text,
                'diccionario': diccionario,
            })
        else:#request("POST")
            status = request.POST.get('status')
            try:
                if status and nro:
                    pedido=PedidoModel.objects.filter(id_nro=restaurante.id,nro=nro,is_pickup=True,is_delivery=False).first()
                    pedido.status=status
                    pedido.save()

                return redirect('detail_pickup',nro=nro)
            except Exception as e:
                # Si hay un error, renderiza la plantilla con los formularios
                return render(request, 'detail_pickup.html', {
                      # Muestra el formulario check con los datos actuales
                    'error': f'Error al guardar los cambios: {str(e)}',
                })
            
def PagoView(request, id, total):
    try:
        id = int(id)  # Asegúrate de que id sea un número
        total = float(total)  # Asegúrate de que total sea un número
    except (ValueError, TypeError):
        return render(request, 'error.html', {'error': 'ID o total no válidos.'})

    mail = request.session.get('email')
    cliente_restaurante = Restaurante.objects.filter(email=mail).first()
    cliente = Cliente.objects.filter(email=mail).first()
    tipo=request.session.get('type')
    if request.session.get('type')==False:#delivery
        request.session['total']=total
    elif request.session.get('type')==True:#Pickup
        request.session['total2']=total
    if request.method == "GET":
        # Si el cliente no ha iniciado sesión
        if not mail:
            id=str(id)
            return redirect('registro_datos',id=id)

        # Si el cliente ha iniciado sesión
        if cliente_restaurante or cliente:
            # Guardar los datos del cliente o restaurante en variables de sesión
            request.session['nombre'] = cliente.nombre if cliente else cliente_restaurante.nombre
            request.session['identificacion'] = cliente.cedula if cliente else cliente_restaurante.rif
            request.session['mail'] = cliente_restaurante.email if cliente_restaurante else cliente.email
            request.session['telefono'] = cliente.telefono if cliente else cliente_restaurante.telefono

            # Encontrar los medios de pago que tiene disponible el restaurante
            restaurante = Restaurante.objects.filter(id=id).first()
            if not restaurante:
                return render(request, 'error.html', {'error': 'Restaurante no encontrado.'})

            pago_nacional = Pago.objects.filter(restaurante=restaurante.id).first()
            zelle = Zelle.objects.filter(restaurante=restaurante.id).first()
            paypal = Paypal.objects.filter(restaurante=restaurante.id).first()

            # Redirigir según el medio de pago disponible
            if pago_nacional:
                if pago_nacional.pagomovil_active:
                    return redirect('pago_movil', id=str(id))
                elif pago_nacional.efectivo_active:
                    return redirect('efectivo', id=str(id))

            if zelle and zelle.zelle_active:
                return redirect('zelle', id=str(id))
            elif paypal and paypal.paypal_active:
                return redirect('paypal', id=str(id))

            # Si no hay medios de pago disponibles
            return render(request, 'pago.html', {
                'nombre': restaurante.id,
                'error': "El restaurante aún no posee medios de pago, lo sentimos."
            })
        else:
            return redirect('registro_datos',id=id)
    
def Registro_datos_view(request,id):
    id=int(id)
    
    restaurante = Restaurante.objects.filter(id=id).first()
    if request.method == "GET":
        request.session['registro']=True
        
        form=Datos_Form(initial={
            'nombre':request.session.get('nombre'),
            'identificacion': request.session.get('identificacion'),
            'email': request.session.get('mail'),
            'telefono': request.session.get('telefono'),
        })
        tipo=request.session.get('type')
        tipo=bool(tipo)
        ubicacion=""
        if tipo==False:
            ubicacion=request.session.get("ubicacion")
            ubicacion=ubicacion.split("+")
            ubicacion=obtener_direccion(ubicacion[0], ubicacion[1])
        return render(request, 'registro_datos.html', 
            {'form': form,
             'ubicacion': ubicacion if ubicacion else False,
             'item': restaurante.id,
             'nombre':restaurante.nombre,
             'reservacion':request.session.get('reservacion') if 'reservacion' in request.session else False,
             'type':request.session.get('type')#True=pickup, False=delivery
             })
    
    if request.method == "POST":
        form = Datos_Form(request.POST)
        if form.is_valid():

            if 'reservacion' in request.session:
                print("SITVE la sesion reservacion")
                mesa = request.session.get('mesa') 
                fecha = request.session.get('fecha') 
                hora = request.session.get('hora')
                personas= request.session.get('puestos')
                    
                print("MESA ",mesa)
                print("fecha ",fecha)
                print("hora ",hora)
                print("personas ",personas)

                fecha = datetime.strptime(fecha, '%Y-%m-%d').date()
                mesa=int(mesa)

            # Obtener las reservaciones
                reservaciones = Reservaciones_horario.objects.filter(restaurante=restaurante.id, fecha=fecha, mesa=mesa).first()

                # Inicializar lista
                if reservaciones is None:
                    lista = []  # Si no hay horas, inicializa como una lista vacía
                else:
                    # Dividir horas en una lista
                    if isinstance(reservaciones.horas, str):
                        lista = reservaciones.horas.split(',') if ',' in reservaciones.horas else [reservaciones.horas]
                    else:
                        lista = list(reservaciones.horas)  # Asegúrate de que esto sea correcto

                    # Encontrar el índice de la hora
                index = None
                for idx, item in enumerate(lista):
                    if item == hora:
                        index = idx
                        break  # Salir del bucle una vez que se encuentra el índice

                    # Manejo del estado
                if isinstance(reservaciones.status, str):
                    status = reservaciones.status.split(',') if ',' in reservaciones.status else [reservaciones.status]
                else:
                    status = list(reservaciones.status)  # Asegúrate de que esto sea correcto

                # Actualizar el estado
                if index is not None:
                    status[index] = '1'  # Cambiar a '1' para indicar que está ocupada
                    reservaciones.status = ','.join(status)
                reservaciones.save()
                    
                nueva_reservacion=Reservacion_cliente(
                    restaurante = restaurante,
                    nombre=form.cleaned_data['nombre'],
                    identificacion=form.cleaned_data['identificacion'],
                    email= form.cleaned_data['email'],
                    telefono=form.cleaned_data['telefono'],
                    fecha=fecha,
                    hora=datetime.strptime(hora, "%H:%M"),
                    mesa=mesa,
                    nro_personas=int(personas),
                )
                if 'reservacion' in request.session:
                    del request.session['reservacion']
                if 'mesa' in request.session:
                    del request.session['mesa']
                if 'fecha' in request.session:
                    del request.session['fecha']
                if 'hora' in request.session:
                    del request.session['hora']
                if 'puestos' in request.session:
                    del request.session['puestos']

                nueva_reservacion.save()
                return redirect('success')

            else:
                request.session['registro'] = True
                request.session['nombre'] = form.cleaned_data['nombre']
                request.session['identificacion'] = form.cleaned_data['identificacion']
                request.session['mail'] = form.cleaned_data['email']
                request.session['telefono'] = form.cleaned_data['telefono']

                pago_nacional = Pago.objects.filter(restaurante=restaurante.id).first()
                zelle = Zelle.objects.filter(restaurante=restaurante.id).first()
                paypal = Paypal.objects.filter(restaurante=restaurante.id).first()

                if pago_nacional and pago_nacional.pagomovil_active:
                    # Construir la URL con los parámetros
                    return redirect('pago_movil',id=str(id))

                elif pago_nacional and pago_nacional.efectivo_active:
                    return redirect('efectivo',id=str(id))

                elif zelle and zelle.zelle_active:
                    return redirect('zelle',id=str(id))

                elif paypal and paypal.paypal_active:
                    return redirect('paypal',id=str(id))

                else:
                    return render(request, 'pago.html', {
                        'nombre': restaurante.nombre,
                        'item': restaurante.id,
                        'pedidos': True if request.session.get('type') else False,
                        'error': "El restaurante aún no posee medios de pago, lo sentimos"
                    })
        else:
            return render(request, 'registro_datos.html', {
                'form': Datos_Form(),
                'error': "Verifique los datos introducidos",
                })

def PagoMovilView(request, id):
    id = int(id)
    if request.session.get('type')==False:#delivery
        total=request.session.get('total')
    elif request.session.get('type')==True:#Pickup
        total=request.session.get('total2')
    if request.session.get('email'):
        request.session['registro']=False
    
    if total is None:
        return render(request, 'pago_movil.html', {'error': 'Total no encontrado en la sesión.'})  # Manejo de error

    if request.method == "GET":
        restaurante = Restaurante.objects.filter(id=id).first()
        if not restaurante:
            return render(request, 'pago_movil.html', {'error': 'Restaurante no encontrado.'})  # Manejo de error

        zelle = Zelle.objects.filter(restaurante=restaurante.id).first()
        paypal = Paypal.objects.filter(restaurante=restaurante.id).first()
        pago_restaurante = Pago.objects.filter(restaurante=restaurante.id).first()
        pago_restaurante.banco=read_banks(pago_restaurante.banco)

        form = PagoMovilForm(initial={ 
            'hora': timezone.now().strftime('%H:%M'),
            'nombre': request.session.get('nombre'), 
            'email': request.session.get('email'), 
            'telefono': request.session.get('telefono')
        })
        bolivares=cambio_dolar(total)
        bolivares=float(bolivares)
        print(bolivares)
        return render(request, 'pago_movil.html', {
            'item': restaurante.id,
            'pago_restaurante': pago_restaurante,
            'nombre': restaurante.nombre,
            'form': form,
            'total': total,
            'bolivares':round(bolivares,2),
            'rif': restaurante.rif,
            'registro': bool(request.session.get('registro')),
            'pedidos': bool(request.session.get('type')),
            'efectivo': pago_restaurante.efectivo_active if pago_restaurante else False,
            'zelle': zelle.zelle_active if zelle else False,
            'paypal': paypal.paypal_active if paypal else False,
            'hora': timezone.localtime(timezone.now()).strftime('%H:%M')
        })
    
    elif request.method == "POST":
        restaurante = Restaurante.objects.filter(id=id).first()
        if not restaurante:
            return render(request, 'pago_movil.html', {'error': 'Restaurante no encontrado.'})  # Manejo de error
        hora=request.POST.get('hora')
        fecha_actual = timezone.now().date()
        form = PagoMovilForm(request.POST)
        if form.is_valid():
            try:
                if request.session.get('elegidos'):
                    notas=[]
                    for i in request.session.get('elegidos').split(','):
                        comentario = request.session.get(f'comentario_{i}', '')
                        if comentario:
                            notas.append(comentario)
                
                if request.session.get('elegidos2'):
                    notas2=[]
                    for i in request.session.get('elegidos2').split(','):
                        comentario2 = request.session.get(f'2comentario_{i}', '')
                        if comentario2:
                            notas2.append(comentario2)
                 # Al registrar un nuevo pedido
                # Crear una nueva instancia de Pedido_Delivery

                if request.session.get('type')==False:#True=pickup, False=delivery
                    nuevo_pedido = PedidoModel(
                        id_nro=restaurante,
                        nro_items=request.session.get('elegidos'),
                        fecha=datetime.combine(fecha_actual, datetime.strptime(hora, '%H:%M').time()),
                        notas=';'.join(notas),
                        cantidades=request.session.get('cantidad'),
                        nombre=request.session.get('nombre'),
                        identificacion=request.session.get('identificacion'),
                        email=request.session.get('mail'),
                        telefono=request.session.get('telefono'),
                        ubicacion=request.session.get('ubicacion'),
                        status=False,
                        monto=total,
                        is_delivery=True,
                        is_pickup=False,
                    )
                elif request.session.get('type')==True:#True=pickup, False=delivery
                    nuevo_pedido = PedidoModel(
                        id_nro=restaurante,
                        nro_items=request.session.get('elegidos2'),
                        fecha=datetime.combine(fecha_actual, datetime.strptime(hora, '%H:%M').time()),
                        notas=';'.join(notas2),
                        cantidades=request.session.get('cantidad2'),
                        nombre=request.session.get('nombre'),
                        identificacion=request.session.get('identificacion'),
                        email=request.session.get('mail'),
                        telefono=request.session.get('telefono'),
                        status=False,
                        monto=total,
                        is_delivery=False,
                        is_pickup=True,
                    )
                nuevo_pedido.save()  # Esto crea un nuevo registro en la base de datos

                # Crear una nueva instancia de PagoMovil
                nuevo_pago = PagoMovil(
                    pedido=nuevo_pedido,  # Asigna la instancia del pedido
                    banco=form.cleaned_data['banco'],
                    monto=total,
                    ref=form.cleaned_data['ref'],
                    titular=form.cleaned_data['nombre'],
                    telefono=form.cleaned_data['telefono'],
                    precio_dolar=cambio_dolar('1'),           
                )
                nuevo_pago.save() 
                    # Guardar el valor de la variable que deseas conservar
                delete_session()
                return redirect('success')
            except Exception as e:
                return render(request,'pago_movil.html',{
                        'error': f"ERROR: {e} ",
                })
       
            # Si el formulario no es válido, imprime los errores para depuración
        print(form.errors)
            # Renderiza de nuevo el formulario con los errores
        return render(request, 'pago_movil.html', {
                'form': form,
                'error': 'Formulario no válido.',
                'registro': request.session.get('registro'),
                'pedidos': bool(request.session.get('type')),
                'total': total,  # Asegúrate de pasar el total de nuevo
                'item': restaurante.id,
                'rif': restaurante.rif,
        })
    
def ZellePagoView(request, id):
    id = int(id)
    if request.session.get('type')==False:#delivery
        total=request.session.get('total')
    elif request.session.get('type')==True:#Pickup
        total=request.session.get('total2')
    if total is None:
        return render(request, 'zelle_pago.html', {'error': 'Total no encontrado en la sesión.'})  # Manejo de error
    restaurante = Restaurante.objects.filter(id=id).first()
    if not restaurante:
        return render(request, 'zelle_pago.html', {'error': 'Restaurante no encontrado.'})  # Manejo de error
    if request.method == "GET":
        
        pago_nacional=Pago.objects.filter(restaurante=restaurante.id).first()
        zelle = Zelle.objects.filter(restaurante=restaurante.id).first()
        paypal = Paypal.objects.filter(restaurante=restaurante.id).first()

        form = PagoZelleForm(initial={ 
            'nombre': request.session.get('nombre'), 
            'email': request.session.get('mail'), 
            'telefono': request.session.get('telefono')
        })
        return render(request, 'zelle_pago.html', {
            'item': restaurante.id,
            'pago_restaurante': zelle,
            'form': form,
            'total': total,
            'rif': restaurante.rif,
            'registro': bool(request.session.get('registro')),
            'pedidos': bool(request.session.get('type')),
            'pago_movil': pago_nacional.pagomovil_active if pago_nacional.pagomovil_active else False,
            'efectivo': pago_nacional.efectivo_active if pago_nacional.efectivo_active else False,
            'zelle': zelle.zelle_active if zelle else False,
            'paypal': paypal.paypal_active if paypal else False,
            'fecha': datetime.today().strftime('%Y-%m-%d'),
            'hora': timezone.localtime(timezone.now()).strftime('%H:%M'),
        })
    
    elif request.method == "POST":
        if not restaurante:
            return render(request, 'zelle_pago.html', {'error': 'Restaurante no encontrado.'})  # Manejo de error
        fecha=request.POST.get('fecha')
        # Convertir la fecha_input a un objeto date 
        fecha = datetime.strptime(fecha, '%Y-%m-%d').date() 
        # Obtener la hora actual 
        hora=request.POST.get('hora')
        hora=datetime.strptime(hora,'%H:%M').time() 
        form = PagoZelleForm(request.POST)
        if form.is_valid():
            try:
                if request.session.get('elegidos'):
                    notas=[]
                    for i in request.session.get('elegidos').split(','):
                        comentario = request.session.get(f'comentario_{i}', '')
                        if comentario:
                            notas.append(comentario)
                
                if request.session.get('elegidos2'):
                    notas2=[]
                    for i in request.session.get('elegidos2').split(','):
                        comentario2 = request.session.get(f'2comentario_{i}', '')
                        if comentario2:
                            notas2.append(comentario2)
                # Al registrar un nuevo pedido
                # Crear una nueva instancia de Pedido_Delivery
                if request.session.get('type')==False:#True=pickup, False=delivery
                    nuevo_pedido = PedidoModel(
                        id_nro=restaurante,
                        nro_items=request.session.get('elegidos'),
                        fecha=datetime.combine(fecha, hora),
                        notas=';'.join(notas),
                        cantidades=request.session.get('cantidad'),
                        nombre=request.session.get('nombre'),
                        identificacion=request.session.get('identificacion'),
                        email=request.session.get('mail'),
                        telefono=request.session.get('telefono'),
                        ubicacion=request.session.get('ubicacion'),
                        status=False,
                        monto=total,
                        is_delivery=True,
                        is_pickup=False,
                    )
                elif request.session.get('type')==True:#True=pickup, False=delivery
                    nuevo_pedido = PedidoModel(
                        id_nro=restaurante,
                        nro_items=request.session.get('elegidos2'),
                        fecha=datetime.combine(fecha, hora),
                        notas=';'.join(notas2),
                        cantidades=request.session.get('cantidad2'),
                        nombre=request.session.get('nombre'),
                        identificacion=request.session.get('identificacion'),
                        email=request.session.get('mail'),
                        telefono=request.session.get('telefono'),
                        status=False,
                        monto=total,
                        is_delivery=False,
                        is_pickup=True,
                    )
                nuevo_pedido.save()  # Esto crea un nuevo registro en la base de datos

                # Crear una nueva instancia de PagoMovil
                nuevo_pago = ZelleModel(
                    pedido=nuevo_pedido,  # Asigna la instancia del pedido
                    monto=total,
                    ref=form.cleaned_data['ref'],
                    titular=form.cleaned_data['nombre'],
                    telefono=form.cleaned_data['telefono'],
                    email=form.cleaned_data['email'],
                    fecha=datetime.combine(fecha, hora),
                    precio_dolar=cambio_dolar('1'), 
                )
                nuevo_pago.save() 
                delete_session()
                return redirect('success')
            except Exception as e:
                return render(request,'zelle_pago.html',{
                        'error': f"ERROR: {e} ",
                        'item': restaurante.id,
                })
       
            # Si el formulario no es válido, imprime los errores para depuración
        print(form.errors)
            # Renderiza de nuevo el formulario con los errores
        return render(request, 'zelle_pago.html', {
                'form': form,
                'error': 'Formulario no válido.',
                'registro': request.session.get('registro'),
                'pedidos': bool(request.session.get('type')),
                'total': total,  # Asegúrate de pasar el total de nuevo
                'item': restaurante.id,
                'rif': restaurante.rif,
        })

def PaypalPagoView(request, id):
    id = int(id)
    if request.session.get('type')==False:#delivery
        total=request.session.get('total')
    elif request.session.get('type')==True:#Pickup
        total=request.session.get('total2')
    
    restaurante = Restaurante.objects.filter(id=id).first()
    if request.method == "GET":
        if not restaurante:
            return render(request, 'paypal_pago.html', {'error': 'Restaurante no encontrado.'})  # Manejo de error
        pago_nacional=Pago.objects.filter(restaurante=restaurante.id).first()
        zelle = Zelle.objects.filter(restaurante=restaurante.id).first()
        paypal = Paypal.objects.filter(restaurante=restaurante.id).first()

        form = PagoPaypalForm(initial={ 
            'nombre': request.session.get('nombre'),
            'hora': timezone.localtime(timezone.now()).strftime('%H:%M'), 
            'email': request.session.get('mail'),
        })
        return render(request, 'paypal_pago.html', {
            'item': restaurante.id,
            'pago_restaurante': paypal,
            'form': form,
            'total': total,
            'rif': restaurante.rif,
            'registro': bool(request.session.get('registro')),
            'pedidos': bool(request.session.get('type')),
            'pago_movil': pago_nacional.pagomovil_active if pago_nacional.pagomovil_active else False,
            'efectivo': pago_nacional.efectivo_active if pago_nacional.efectivo_active else False,
            'zelle': zelle.zelle_active if zelle else False,
            'paypal': paypal.paypal_active if paypal else False,
            'fecha': datetime.today().strftime('%Y-%m-%d'),
            'hora': timezone.localtime(timezone.now()).strftime('%H:%M'),
        })
    
    elif request.method == "POST":
        if not restaurante:
            return render(request, 'paypal_pago.html', {'error': 'Restaurante no encontrado.'})  # Manejo de error
        fecha=request.POST.get('fecha')
        # Convertir la fecha_input a un objeto date 
        fecha = datetime.strptime(fecha, '%Y-%m-%d').date() 
        hora=request.POST.get('hora')
        hora=datetime.strptime(hora,'%H:%M').time() 

        form = PagoPaypalForm(request.POST)
        if form.is_valid():
            try:
                if request.session.get('elegidos'):
                    notas=[]
                    for i in request.session.get('elegidos').split(','):
                        comentario = request.session.get(f'comentario_{i}', '')
                        if comentario:
                            notas.append(comentario)
                
                if request.session.get('elegidos2'):
                    notas2=[]
                    for i in request.session.get('elegidos2').split(','):
                        comentario2 = request.session.get(f'2comentario_{i}', '')
                        if comentario2:
                            notas2.append(comentario2)
                # Al registrar un nuevo pedido
                # Crear una nueva instancia de Pedido_Delivery
                if request.session.get('type')==False:#True=pickup, False=delivery
                    nuevo_pedido = PedidoModel(
                        id_nro=restaurante,
                        nro_items=request.session.get('elegidos'),
                        fecha=datetime.combine(fecha,hora),
                        notas=';'.join(notas),
                        cantidades=request.session.get('cantidad'),
                        nombre=request.session.get('nombre'),
                        identificacion=request.session.get('identificacion'),
                        email=request.session.get('mail'),
                        telefono=request.session.get('telefono'),
                        ubicacion=request.session.get('ubicacion'),
                        status=False,
                        monto=total,
                        is_delivery=True,
                        is_pickup=False,
                    )
                elif request.session.get('type')==True:#True=pickup, False=delivery
                    nuevo_pedido = PedidoModel(
                        id_nro=restaurante,
                        nro_items=request.session.get('elegidos2'),
                        fecha=datetime.combine(fecha,hora),
                        notas=';'.join(notas2),
                        cantidades=request.session.get('cantidad2'),
                        nombre=request.session.get('nombre'),
                        identificacion=request.session.get('identificacion'),
                        email=request.session.get('mail'),
                        telefono=request.session.get('telefono'),
                        status=False,
                        monto=total,
                        is_delivery=False,
                        is_pickup=True,
                    )
                nuevo_pedido.save()  # Esto crea un nuevo registro en la base de datos

                # Crear una nueva instancia de PagoMovil
                nuevo_pago = PaypalModel(
                    pedido=nuevo_pedido,  # Asigna la instancia del pedido
                    monto=total,
                    ref=form.cleaned_data['ref'],
                    titular=form.cleaned_data['nombre'],
                    email=form.cleaned_data['email'],
                    fecha=datetime.combine(fecha, hora),
                    precio_dolar=cambio_dolar('1'), 
                )
                nuevo_pago.save() 
                    # Guardar el valor de la variable que deseas conservar
                delete_session()
                return redirect('success')
            except Exception as e:
                return render(request,'paypal_pago.html',{
                        'error': f"ERROR: {e} ",
                        'item': restaurante.id,
                })
       
            # Si el formulario no es válido, imprime los errores para depuración
        print(form.errors)
            # Renderiza de nuevo el formulario con los errores
        return render(request, 'paypal_pago.html', {
                'form': form,
                'error': 'Formulario no válido.',
                'registro': request.session.get('registro'),
                'pedidos': bool(request.session.get('type')),
                'total': total,  # Asegúrate de pasar el total de nuevo
                'item': restaurante.id,
                'rif': restaurante.rif,
        })

def EfectivoPagoView(request,id):
    restaurante=Restaurante.objects.filter(id=id).first()
    pago_nacional=Pago.objects.filter(restaurante=restaurante.id).first()
    zelle = Zelle.objects.filter(restaurante=restaurante.id).first()
    paypal = Paypal.objects.filter(restaurante=restaurante.id).first()

    print('TYPE ',request.session.get('type'))
    if request.session.get('type')==False:#delivery
        total=request.session.get('total')
    elif request.session.get('type')==True:#Pickup
        total=request.session.get('total2')
    print('TOTAL ',total)

    if request.method=="GET":
        return render(request,'pago_efectivo.html',{
            'form':EfectivoForm(),
            'nombre':restaurante.nombre,
            'item': restaurante.id,
            'registro': bool(request.session.get('registro')),
            'type': bool(request.session.get('type')),
            'pago_movil': pago_nacional.pagomovil_active if pago_nacional.pagomovil_active else False,
            'zelle': zelle.zelle_active if zelle else False,
            'paypal': paypal.paypal_active if paypal else False,
            'total':total,
        })
    elif request.method=="POST":
        form=EfectivoForm(request.POST)
        if form.is_valid():
            billetes=[
                int(form.cleaned_data['uno']),
                int(form.cleaned_data['cinco']),
                int(form.cleaned_data['diez']),
                int(form.cleaned_data['veinte']),
                int(form.cleaned_data['cincuenta']),
                int(form.cleaned_data['cien']),
            ]
            print("Billetes", billetes)
            billetes2=[
                billetes[0],
                billetes[1]*5,
                billetes[2]*10,
                billetes[3]*20,
                billetes[4]*50,
                billetes[5]*100,
            ]
            suma=sum(billetes2)
            print("SUma ",suma)
            
            if suma==0:
                return render(request,'pago_efectivo.html',{
                    'error': 'Por favor, ingrese la cantidad de dólares que posee para poder procesar el pago.',
                    'form':EfectivoForm(),
                    'nombre':restaurante.nombre,
                    'registro': bool(request.session.get('registro')),
                    'type': bool(request.session.get('type')),
                    'pago_movil': pago_nacional.pagomovil_active if pago_nacional.pagomovil_active else False,
                    'zelle': zelle.zelle_active if zelle else False,
                    'paypal': paypal.paypal_active if paypal else False,
                    'total':total,
                    'item': restaurante.id,
                })
            elif suma<total:
                return render(request,'pago_efectivo.html',{
                    'error': 'La cantidad de dinero ingresada no es suficiente para cubrir el monto del pedido.',
                    'form':EfectivoForm(),
                    'nombre':restaurante.nombre,
                    'registro': bool(request.session.get('registro')),
                    'type': bool(request.session.get('type')),
                    'pago_movil': pago_nacional.pagomovil_active if pago_nacional.pagomovil_active else False,
                    'zelle': zelle.zelle_active if zelle else False,
                    'paypal': paypal.paypal_active if paypal else False,
                    'total':total,
                    'item': restaurante.id,
                })
            elif total<=25 and billetes[5]!=0:
                return render(request,'pago_efectivo.html',{
                    'error': 'Se aceptarán billetes de hasta $50 para pedidos menores a $25',
                    'form':EfectivoForm(),
                    'nombre':restaurante.nombre,
                    'registro': bool(request.session.get('registro')),
                    'type': bool(request.session.get('type')),
                    'pago_movil': pago_nacional.pagomovil_active if pago_nacional.pagomovil_active else False,
                    'zelle': zelle.zelle_active if zelle else False,
                    'paypal': paypal.paypal_active if paypal else False,
                    'total':total,
                    'item': restaurante.id,
                })
            else:#registrar pago
                try:
                    if request.session.get('elegidos'):
                        notas=[]
                        for i in request.session.get('elegidos').split(','):
                            comentario = request.session.get(f'comentario_{i}', '')
                            if comentario:
                                notas.append(comentario)
                
                    if request.session.get('elegidos2'):
                        notas2=[]
                        for i in request.session.get('elegidos2').split(','):
                            comentario2 = request.session.get(f'2comentario_{i}', '')
                            if comentario2:
                                notas2.append(comentario2)
                    # Al registrar un nuevo pedido
                    # Crear una nueva instancia de Pedido_Delivery
                    if request.session.get('type')==False:#True=pickup, False=delivery
                        nuevo_pedido = PedidoModel(
                            id_nro=restaurante,
                            nro_items=request.session.get('elegidos'),
                            fecha=timezone.now(),
                            notas=';'.join(notas),
                            cantidades=request.session.get('cantidad'),
                            nombre=request.session.get('nombre'),
                            identificacion=request.session.get('identificacion'),
                            email=request.session.get('mail'),
                            telefono=request.session.get('telefono'),
                            ubicacion=request.session.get('ubicacion'),
                            status=False,
                            monto=total,
                            is_delivery=True,
                            is_pickup=False,
                        )
                    elif request.session.get('type')==True:#True=pickup, False=delivery
                        nuevo_pedido = PedidoModel(
                            id_nro=restaurante,
                            nro_items=request.session.get('elegidos2'),
                            fecha=timezone.now(),
                            notas=';'.join(notas2),
                            cantidades=request.session.get('cantidad2'),
                            nombre=request.session.get('nombre'),
                            identificacion=request.session.get('identificacion'),
                            email=request.session.get('mail'),
                            telefono=request.session.get('telefono'),
                            monto=total,
                            is_delivery=False,
                            is_pickup=True,
                        )
                    nuevo_pedido.save()  # Esto crea un nuevo registro en la base de datos

                    # Crear una nueva instancia de PagoMovil
                    nuevo_pago = PagoEfectivo(
                        pedido=nuevo_pedido,  # Asigna la instancia del pedido
                        monto=total,
                        billetes=','.join(map(str, billetes)),
                    )
                    nuevo_pago.save() 
                        # Guardar el valor de la variable que deseas conservar
                    delete_session()
                    return redirect('success')
                
                except Exception as e:
                    return render(request,'pago_efectivo.html',{
                            'error': f"ERROR: {e} ",
                            'form':EfectivoForm(),
                            'nombre':restaurante.nombre,
                            'registro': bool(request.session.get('registro')),
                            'type': bool(request.session.get('type')),
                            'pago_movil': pago_nacional.pagomovil_active if pago_nacional.pagomovil_active else False,
                            'zelle': zelle.zelle_active if zelle else False,
                            'paypal': paypal.paypal_active if paypal else False,
                            'total':total,
                            'item': restaurante.id,
                    })

def ReservacionesFechaView(request):
    id=int(request.session.get('restaurante'))
    personas=int(request.session.get('puestos'))
    restaurante = Restaurante.objects.filter(id=id).first()
    reservacion = Reservaciones_config.objects.filter(restaurante=restaurante.id).first()
    pandd = Pickup_Delivery.objects.filter(restaurante=restaurante.id).first()

    if not restaurante:
        raise Restaurante.DoesNotExist
    if request.method == 'GET':
            # Procesar las mesas
         # Obtener la configuración de reservaciones y la opción de entrega/pickup
         

        # Procesar las mesas
        reservacion.mesas = reservacion.mesas.split(',')
        reservacion.mesas = [int(valor) for valor in reservacion.mesas]  
        # Encontrar mesas disponibles
        # Inicializar la lista de índices
        index = []

        # Encontrar mesas disponibles
        for i in range(len(reservacion.mesas)):
            if reservacion.mesas[i] >= int(personas):
                index.append(i)  # Indica la posición de la lista reservacion.mesas
        disponible=[]
        # Recopilar fechas de reservaciones para las mesas disponibles
        lista = {}
        for idx in index:
            # Obtener el número de mesa
            # Obtener las fechas asociadas a la mesa
            idx=int(idx)

            fechas = Reservaciones_horario.objects.filter(restaurante=restaurante, mesa=idx).all()
            if fechas:
                for item in fechas:
                    if ',' in item.status:
                        status=item.status.split(',')
                        for a in status:
                            if a=='0':
                                disponible.append(item.mesa)
                        if disponible:
                            fecha_formateada = item.fecha.strftime('%Y-%m-%d')
                            fecha_formateada=str(fecha_formateada)
                                
                                # Asegurarse de que la clave exista en el diccionario
                            if fecha_formateada not in lista:
                                lista[fecha_formateada]=""  # Inicializar como lista si no existe
                                # Agregar el número de mesa a la lista de esa fecha
                            if lista[fecha_formateada] =="":
                                lista[fecha_formateada]+=str(disponible[0])
                            else:
                                lista[fecha_formateada]+=','+str(disponible[0])
                    else:
                        if item.status == "0":  # Si la mesa está disponible
                            fecha_formateada = item.fecha.strftime('%Y-%m-%d')
                            fecha_formateada=str(fecha_formateada)
                            
                            # Asegurarse de que la clave exista en el diccionario
                            if fecha_formateada not in lista:
                                lista[fecha_formateada] =""  # Inicializar como lista si no existe
                            # Agregar el número de mesa a la lista de esa fecha
                            if lista[fecha_formateada] =="":
                                lista[fecha_formateada]+=str(item.mesa)
                            else:
                                lista[fecha_formateada]+=','+str(item.mesa)
                disponible.clear()

        # Imprimir el resultado
        print("MESAS Y FECHAS ", lista)
        # Obtener la mesa mayor
        mayor = max(reservacion.mesas)
        return render(request, 'reser_fecha.html', {
                    'restaurante': restaurante,
                    'delivery': pandd.active_delivery if pandd else False,
                    'pickup': pandd.active_pickup if pandd else False,
                    'reservaciones': reservacion.active if reservacion else False,
                    'mayor':mayor,
                    'persona': int(personas),
                    'personas': list(range(1, mayor + 1)),
                    'mesas': lista,
        })
    elif request.method == 'POST':
        personas2 = request.POST.get('personas')
        fecha = request.POST.get('fecha')
        mesas=""

        if fecha:
            fecha=str(fecha)
            fecha=fecha.split('+')
            mesas=str(fecha[1])
            fecha=str(fecha[0])

            print("Datos recibidos:")
            print("Personas:", personas2)
            print("Fecha:", fecha)
            print("Mesa: ",mesas)

        if mesas and personas2 and fecha:
            if ',' in mesas:
                mesas=mesas.split(',')
                mesas=str(mesas[0])

            print("MESAS POST: ", mesas)
            print("PERSONAS POST: ", personas2)
            print("FECHA POST: ", fecha)

            # Validar que 'personas2' y 'personas' sean enteros
           
            if int(personas2) != int(personas):
                    request.session['puestos'] = personas2
                    return redirect('presentacion_two', item=restaurante.id)
            

            # Verificar que todos los datos necesarios estén presentes
            elif personas2 and fecha and mesas:
                request.session['puestos'] = personas2
                request.session['mesa'] = mesas
                request.session['fecha'] = fecha
                print("MESA: ", mesas)
                return redirect('reser_hora')
        else:
            return render(request, 'reser_fecha.html', {
                'error': "Revise los datos",
                'restaurante': restaurante,
                'delivery': pandd.active_delivery if pandd else False,
                'pickup': pandd.active_pickup if pandd else False,
            })
        
def ReservacionesHoraView(request):
    id = request.session.get('restaurante')
    personas = request.session.get('puestos')

    if id is None or personas is None:
        return render(request, 'error.html', {'message': 'Datos de sesión no válidos.'})

    id = int(id)
    personas = int(personas)
    print("ID ",id)
    restaurante = Restaurante.objects.filter(id=id).first()
    if not restaurante:
        return render(request, 'error.html', {'message': 'Restaurante no encontrado.'})

    if request.method == 'GET':
        
            # Procesar las mesas
         # Obtener la configuración de reservaciones y la opción de entrega/pickup
        reservacion = Reservaciones_config.objects.filter(restaurante=restaurante.id).first()
        pandd = Pickup_Delivery.objects.filter(restaurante=restaurante.id).first() 

        # Procesar las mesas
        reservacion.mesas = reservacion.mesas.split(',')
        reservacion.mesas = [int(valor) for valor in reservacion.mesas]  
        # Encontrar mesas disponibles
        # Inicializar la lista de índices
        index = []

        # Encontrar mesas disponibles
        for i in range(len(reservacion.mesas)):
            if reservacion.mesas[i] >= int(personas):
                index.append(i)  # Indica la posición de la lista reservacion.mesas
        disponible=[]
        # Recopilar fechas de reservaciones para las mesas disponibles
        lista = {}
        for idx in index:
            # Obtener el número de mesa
            # Obtener las fechas asociadas a la mesa
            idx=int(idx)

            fechas = Reservaciones_horario.objects.filter(restaurante=restaurante,mesa=idx).all()
            if fechas:
                for item in fechas:
                    if ',' in item.status:
                        status=item.status.split(',')
                        for a in status:
                            if a=='0':
                                disponible.append(item.mesa)
                        if disponible:
                            fecha_formateada = item.fecha.strftime('%Y-%m-%d')
                            fecha_formateada=str(fecha_formateada)
                                
                                # Asegurarse de que la clave exista en el diccionario
                            if fecha_formateada not in lista:
                                lista[fecha_formateada]=""  # Inicializar como lista si no existe
                                # Agregar el número de mesa a la lista de esa fecha
                            if lista[fecha_formateada] =="":
                                lista[fecha_formateada]+=str(disponible[0])
                            else:
                                lista[fecha_formateada]+=','+str(disponible[0])
                    else:
                        if item.status == "0":  # Si la mesa está disponible
                            fecha_formateada = item.fecha.strftime('%Y-%m-%d')
                            fecha_formateada=str(fecha_formateada)
                            
                            # Asegurarse de que la clave exista en el diccionario
                            if fecha_formateada not in lista:
                                lista[fecha_formateada] =""  # Inicializar como lista si no existe
                            # Agregar el número de mesa a la lista de esa fecha
                            if lista[fecha_formateada] =="":
                                lista[fecha_formateada]+=str(item.mesa)
                            else:
                                lista[fecha_formateada]+=','+str(item.mesa)
                disponible.clear()
        print("LISTA FECHAS Y MESAS:  ",lista)
        # Obtener la fecha de la sesión
        date = request.session.get('fecha')
        date = datetime.strptime(date,'%Y-%m-%d').date()
        print("DATE, ",date)
        # Obtener la mesa elegida
        table = request.session.get('mesa')
        table=int(table)
        print("MESA ELEGIDA ", table)
        lista_horas=[]
        # Obtener las horas asociadas a la mesa y la fecha
        horas = Reservaciones_horario.objects.filter(restaurante=id,mesa=table,fecha=date).first()
        print("HORAS OBJECT ",horas)
        if horas:
            print('HORAS ',horas.horas)
            print("STATUs ",horas.status)
            print("FECHA ",horas.fecha)
            print("MESA ",horas.mesa)
        
            if ',' in horas.horas:
                lista_horas=horas.horas.split(',')
            else:
                lista_horas=[horas.horas]

            if ',' in horas.status:
                lista_status=horas.status.split(',')
            else:
                lista_status=[horas.status]

            print("LISTA HORA ",lista_horas)
            print("STATUS ",lista_status)
            for i in range(len(lista_status)):
                if lista_status[i]=='1':
                    del lista_horas[i]

            print("lista horas ",lista_horas)
            # Obtener el mayor número de mesas
        mayor = max(reservacion.mesas) if reservacion.mesas else 0

        return render(request, 'reser_hora.html', {
            'restaurante': restaurante,
            'delivery': pandd.active_delivery if pandd else False,
            'pickup': pandd.active_pickup if pandd else False,
            'reservaciones': reservacion.active if reservacion else False,
            'mayor': mayor,            
            'date': date.strftime('%Y-%m-%d'),
            'persona': int(personas),
            'personas': list(range(1, mayor + 1)),
            'mesas': lista,
            'horas':  lista_horas if lista_horas else False,
        })

    elif request.method == 'POST':
        fecha = request.POST.get('fecha')
        
        fecha=str(fecha)
        fecha=fecha.split('+')
        mesas=str(fecha[1])
        fecha=str(fecha[0])

        personas2 = request.POST.get('personas')

        mesa = request.POST.get('mesa')

        if ',' in mesas:
            mesas=mesas.split(',')
            mesas=str(mesas[0])

        hora = request.POST.get('hora')

        fecha1=request.session.get("fecha")
        mesa1=request.session.get("mesa")
        print("FECHA POST ",fecha)
        print("mesas POST ",mesas)
        print("personass POST ",personas2,'\n')
        print("FECHA SESSION ",fecha1)
        print("mesas SESSION ",mesa1)
        print("personass SESSION ",personas,'\n')

        # Verificar si las personas o la fecha han cambiado
        if int(personas)!=int(personas2) or fecha1 != fecha or mesa1!=mesas:
            request.session['puestos'] = personas
            request.session['fecha'] = fecha
            request.session['mesa']=mesas
            return redirect('reser_fecha')  # Asegúrate de que esta URL esté definida en tu urls.py

        elif personas2 and fecha and mesas:
            
            mail=request.session.get('email')
            if mail:
                # Convertir la fecha
                fecha = datetime.strptime(fecha, '%Y-%m-%d').date()

                # Obtener las reservaciones
                reservaciones = Reservaciones_horario.objects.filter(restaurante=restaurante.id, fecha=fecha, mesa=mesas).first()

                # Inicializar lista
                if reservaciones is None:
                    lista = []  # Si no hay horas, inicializa como una lista vacía
                else:
                    # Dividir horas en una lista
                    if isinstance(reservaciones.horas, str):
                        lista = reservaciones.horas.split(',') if ',' in reservaciones.horas else [reservaciones.horas]
                    else:
                        lista = list(reservaciones.horas)  # Asegúrate de que esto sea correcto

                # Encontrar el índice de la hora
                index = None
                for idx, item in enumerate(lista):
                    if item == hora:
                        index = idx
                        break  # Salir del bucle una vez que se encuentra el índice

                # Manejo del estado
                if isinstance(reservaciones.status, str):
                    status = reservaciones.status.split(',') if ',' in reservaciones.status else [reservaciones.status]
                else:
                    status = list(reservaciones.status)  # Asegúrate de que esto sea correcto

                # Actualizar el estado
                if index is not None:
                    status[index] = '1'  # Cambiar a '1' para indicar que está ocupada
                    reservaciones.status = ','.join(status)
                reservaciones.save()
                
                cliente_restaurante = Restaurante.objects.filter(email=mail).first()
                cliente = Cliente.objects.filter(email=mail).first()

                nueva_reservacion=Reservacion_cliente(
                    restaurante = restaurante,
                    nombre=cliente.nombre if cliente else cliente_restaurante.nombre,
                    identificacion=cliente.cedula if cliente else cliente_restaurante.rif,
                    email= mail,
                    telefono=cliente.telefono if cliente else cliente_restaurante.telefono,
                    fecha=fecha,
                    hora=hora,
                    mesa=mesas,
                    nro_personas=personas2,
                )
                nueva_reservacion.save()
                return redirect('success')
            else:
                print("mesas",mesas)
                request.session['puestos'] = personas
                request.session['mesa'] = mesas
                request.session['fecha'] = fecha
                request.session['hora'] = hora
                request.session['reservacion']=True

                return redirect('registro_datos',id=restaurante.id)
        else:
            return render(request, 'reser_hora.html', {
                'error': "Revise los datos",
            })

def VerReservaView(request,param1,param2,param3):
    fecha=datetime.strptime(param1, '%Y-%m-%d').date() 
    mesa=int(param2)
    hora=datetime.strptime(param3, "%H:%M")

    mail = request.session.get('email')
    if not mail:
        return render(request, 'usuario_sesion/login.html', {
            'form': IniciarSesion(),
            'error': 'Email o contraseña incorrecto'
        })
    else:
        restaurante=Restaurante.objects.filter(email=mail).first()
        if request.method=="GET":
            reserva=Reservacion_cliente.objects.filter(restaurante=restaurante,fecha=fecha,hora=hora,mesa=mesa).first()
            return render(request,'detail_reserva.html',{
                'reserva': reserva,
                'nombre':restaurante.nombre,
            })

def SuccessView(request):
    if request.method=="GET":
        return render(request,'success.html',{
            'texto':'Operacion procesada con exito',
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


def cambio_dolar(monto):
    monto = float(monto)

    url = 'https://pydolarve.org/api/v1/dollar/conversion'
    params = {
        'type': 'USD',
        'value': monto,
        'page': 'bcv',
        'monitor': 'usd'
    }
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.get(url, params=params, headers=headers)
    
    # Check if the response was successful
    if response.status_code == 200:        
        return (response.text)  # Adjust this key based on the actual response structure
    else:
        print(f"Error: {response.status_code}")
        return None

def obtener_direccion(param1,param2):
    param1=str(param1)
    param2=str(param2)
    geolocator = Nominatim(user_agent="MealMate")
    location = geolocator.reverse(f"{param1}, {param2}")
    return location.address

def delete_session(request):
    valor_a_conservar = request.session.get('email')
    ubicacion = request.session.get('ubicacion')
    timestamp=request.session.get('timestamp')
             #vaciar todas las variables de sesión
    request.session.flush()

                # Restaurar la variable que deseas conservar
    request.session['email'] = valor_a_conservar
    request.session['ubicacion'] = ubicacion
    request.session['timestamp'] = timestamp