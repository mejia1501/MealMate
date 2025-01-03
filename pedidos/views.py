from django.shortcuts import render,redirect
from .models import Pedido_Delivery,ZelleModel,PagoNacional,PaypalModel,Pedido_Pickup
from user_r.models import Restaurante,Menu,Ingredientes,Pago,Paypal,Zelle
from usuario_sesion.models import Cliente
from usuario_sesion.forms import IniciarSesion
from .forms import Datos_Form,PagoMovilForm,PagoPaypalForm,PagoZelleForm
from django.utils import timezone
import datetime
import csv
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
            pedido=Pedido_Delivery.objects.filter(id_nro=restaurante.id,nro=nro).first()

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
                    }

            total = sum(item['precio'] for item in detalles_items.values())  # Sumar todos los totales
            iva = total + (total * 0.16)  # Total con IVA

            #pago,nro=nro de pedido

            pago_nacional=PagoNacional.objects.filter(pedido=nro,id_nro=restaurante.id).first()
            zelle=ZelleModel.objects.filter(pedido=nro,id_nro=restaurante.id).first()
            paypal=PaypalModel.objects.filter(pedido=nro,id_nro=restaurante.id).first()

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

            return render(request, 'detail_delivery.html',{
                'pedidos':pedido,
                'nombre':restaurante.nombre,
                'detalles':detalles_items,
                'subtotal': round(total, 2),
                'iva': round(iva, 2),
                'pago':pago,
                'text':text,
            })
        else:#request("POST")
            status = request.POST.get('status')
            try:

                if status and nro:
                    pedido=Pedido_Delivery.objects.filter(nro=nro,id_nro=restaurante.id).first()
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
            pedido=Pedido_Pickup.objects.filter(id_nro=restaurante.id,nro=nro).first()

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
                    }

            total = sum(item['precio'] for item in detalles_items.values())  # Sumar todos los totales
            iva = total + (total * 0.16)  # Total con IVA

            #pago,nro=nro de pedido

            pago_nacional=PagoNacional.objects.filter(pedido=nro,id_nro=restaurante.id).first()
            zelle=ZelleModel.objects.filter(pedido=nro,id_nro=restaurante.id).first()
            paypal=PaypalModel.objects.filter(pedido=nro,id_nro=restaurante.id).first()

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

            return render(request, 'detail_pickup.html',{
                'pedidos':pedido,
                'nombre':restaurante.nombre,
                'detalles':detalles_items,
                'subtotal': round(total, 2),
                'iva': round(iva, 2),
                'pago':pago,
                'text':text,
            })
        else:#request("POST")
            status = request.POST.get('status')
            try:

                if status and nro:
                    pedido=Pedido_Delivery.objects.filter(nro=nro,id_nro=restaurante.id).first()
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
    print("tipo",tipo)
    print("toatal",total)
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
        return render(request, 'registro_datos.html', 
            {'form': form,
             'ubicacion':request.session.get('ubicacion'),
             'item': restaurante.id,
             'nombre':restaurante.nombre,
             'type':request.session.get('type')#True=pickup, False=delivery
             })
    
    if request.method == "POST":
        form = Datos_Form(request.POST)
        if form.is_valid():
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
    tipo=request.session.get('type')
    if request.session.get('type')==False:#delivery
        total=request.session.get('total')
    elif request.session.get('type')==True:#Pickup
        total=request.session.get('total2')
    
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

        return render(request, 'pago_movil.html', {
            'item': restaurante.id,
            'pago_restaurante': pago_restaurante,
            'form': form,
            'total': total,
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
                notas=[]
                for i in request.session['elegidos'].split(','):
                    comentario = request.session.get(f'comentario_{i}', '')
                    if comentario:
                        notas.append(comentario)
                notas2=[]
                for i in request.session['elegidos2'].split(','):
                    comentario = request.session.get(f'2comentario_{i}', '')
                    if comentario:
                        notas2.append(comentario)
                 # Al registrar un nuevo pedido
                # Crear una nueva instancia de Pedido_Delivery
                if request.session.get('type')==False:#True=pickup, False=delivery
                    nuevo_pedido = Pedido_Delivery(
                        id_nro=restaurante,
                        nro_items=request.session.get('elegidos'),
                        fecha=datetime.datetime.combine(fecha_actual, datetime.datetime.strptime(hora, '%H:%M').time()),
                        notas=';'.join(notas),
                        cantidades=request.session.get('cantidad'),
                        nombre=request.session.get('nombre'),
                        identificacion=request.session.get('identificacion'),
                        email=request.session.get('mail'),
                        telefono=request.session.get('telefono'),
                        ubicacion=request.session.get('ubicacion'),
                        status=False,
                        monto=total
                    )
                elif request.session.get('type')==True:#True=pickup, False=delivery
                    nuevo_pedido = Pedido_Pickup(
                        id_nro=restaurante,
                        nro_items=request.session.get('elegidos2'),
                        fecha=datetime.datetime.combine(fecha_actual, datetime.datetime.strptime(hora, '%H:%M').time()),
                        notas=';'.join(notas2),
                        cantidades=request.session.get('cantidad2'),
                        nombre=request.session.get('nombre'),
                        identificacion=request.session.get('identificacion'),
                        email=request.session.get('mail'),
                        telefono=request.session.get('telefono'),
                        ubicacion=request.session.get('ubicacion'),
                        status=False
                    )
                nuevo_pedido.save()  # Esto crea un nuevo registro en la base de datos

                # Crear una nueva instancia de PagoNacional
                nuevo_pago = PagoNacional(
                    id_nro=restaurante,
                    pedido=nuevo_pedido.nro,  # Asigna la instancia del pedido
                    is_pagomovil=True,
                    banco=form.cleaned_data['banco'],
                    monto=total,
                    ref=form.cleaned_data['ref'],
                    titular=form.cleaned_data['nombre'],
                    telefono=form.cleaned_data['telefono'],
                    is_efectivo=False
                )
                nuevo_pago.save() 
                    # Guardar el valor de la variable que deseas conservar
                valor_a_conservar = request.session.get('email')
                    # Vaciar todas las variables de sesión
                request.session.flush()
                    # Restaurar la variable que deseas conservar
                request.session['email'] = valor_a_conservar
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
    if request.method == "GET":
        if not restaurante:
            return render(request, 'zelle_pago.html', {'error': 'Restaurante no encontrado.'})  # Manejo de error
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
        })
    
    elif request.method == "POST":
        if not restaurante:
            return render(request, 'zelle_pago.html', {'error': 'Restaurante no encontrado.'})  # Manejo de error
        fecha=request.POST.get('fecha')
        # Convertir la fecha_input a un objeto date 
        fecha = datetime.datetime.strptime(fecha, '%Y-%m-%d').date() 
        # Obtener la hora actual 
        hora_actual = timezone.now().time()
        form = PagoZelleForm(request.POST)
        if form.is_valid():
            try:
                notas=[]
                for i in request.session['elegidos'].split(','):
                    comentario = request.session.get(f'comentario_{i}', '')
                    if comentario:
                        notas.append(comentario)
                # Al registrar un nuevo pedido
                # Crear una nueva instancia de Pedido_Delivery
                if request.session.get('type')==False:#True=pickup, False=delivery
                    nuevo_pedido = Pedido_Delivery(
                        id_nro=restaurante,
                        nro_items=request.session.get('elegidos'),
                        fecha=datetime.datetime.combine(fecha, hora_actual),
                        notas=';'.join(notas),
                        cantidades=request.session.get('cantidad'),
                        nombre=request.session.get('nombre'),
                        identificacion=request.session.get('identificacion'),
                        email=request.session.get('mail'),
                        telefono=request.session.get('telefono'),
                        ubicacion=request.session.get('ubicacion'),
                        status=False,
                        monto=total
                    )
                elif request.session.get('type')==True:#True=pickup, False=delivery
                    nuevo_pedido = Pedido_Pickup(
                        id_nro=restaurante,
                        nro_items=request.session.get('elegidos'),
                        fecha=datetime.datetime.combine(fecha, hora_actual),
                        notas=';'.join(notas),
                        cantidades=request.session.get('cantidad'),
                        nombre=request.session.get('nombre'),
                        identificacion=request.session.get('identificacion'),
                        email=request.session.get('mail'),
                        telefono=request.session.get('telefono'),
                        ubicacion=request.session.get('ubicacion'),
                        status=False
                    )
                nuevo_pedido.save()  # Esto crea un nuevo registro en la base de datos

                # Crear una nueva instancia de PagoNacional
                nuevo_pago = ZelleModel(
                    id_nro=restaurante,
                    pedido=nuevo_pedido.nro,  # Asigna la instancia del pedido
                    monto=total,
                    ref=form.cleaned_data['ref'],
                    titular=form.cleaned_data['nombre'],
                    telefono=form.cleaned_data['telefono'],
                    email=form.cleaned_data['email'],
                    fecha=form.cleaned_data['fecha'],
                )
                nuevo_pago.save() 
                    # Guardar el valor de la variable que deseas conservar
                valor_a_conservar = request.session.get('email')
                    # Vaciar todas las variables de sesión
                request.session.flush()
                    # Restaurar la variable que deseas conservar
                request.session['email'] = valor_a_conservar
                return redirect('success')
            except Exception as e:
                return render(request,'zelle_pago.html',{
                        'error': f"ERROR: {e} ",
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

def SuccessView(request):
    if request.method=="GET":
        return render(request,'success.html',{
            'texto':'Su pedido ha sido procesado con exito',
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