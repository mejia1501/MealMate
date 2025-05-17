from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import CreateNewRestauranteForm, IniciarSesion, CreateNewClientForm, CuentaCliente
from user_r.models import Restaurante, Cliente,Menu
from pedidos.models import PedidoModel, PagoMovil,PagoEfectivo,PaypalModel,ZelleModel
from pedidos.views import cambio_dolar,obtener_ingredientes
from servicios.models import Reservacion_cliente
from django.utils import timezone
from django.contrib import messages
import pytz
from datetime import datetime, timedelta
from django.contrib.auth.hashers import make_password, check_password
import csv
# Define the timezone
zona_horaria = pytz.timezone('America/Caracas')

def check_user_activity(user):
    """Check if the user has been inactive for the defined period."""
    INACTIVITY_PERIOD = timedelta(days=30)
    if user.last_login + INACTIVITY_PERIOD < datetime.now(zona_horaria):
        user.is_active = False
        user.save()
        return True
    return False


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

def iniciar_sesion(request):
    # Clear specific session variables
    session_keys = ['registro', 'nombre', 'identificacion', 'mail', 'telefono']
    for key in session_keys:
        request.session.pop(key, None)

    email = request.session.get('email')
    if email:
        cliente = Cliente.objects.filter(email=email).first()
        restaurante = Restaurante.objects.filter(email=email).first()

        if cliente:
            request.session['tipo']=False
            if check_user_activity(cliente):
                valor_a_conservar = request.session.get('ubicacion')
                request.session.flush()
                if valor_a_conservar is not None:
                    request.session['ubicacion'] = valor_a_conservar
                        
        elif restaurante:
            request.session['tipo']=True
            if check_user_activity(restaurante):
                valor_a_conservar = request.session.get('ubicacion')
                request.session.flush()
                if valor_a_conservar is not None:
                    request.session['ubicacion'] = valor_a_conservar

        # Retain the 'ubicacion' variable if it exists
        
    if request.method == 'GET':
        return render(request, 'usuario_sesion/login.html', {
                'form': IniciarSesion()
            })
    else:
        form=IniciarSesion(request.POST)
            
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

        if not email or not password:
            return render(request, 'usuario_sesion/login.html', {
                    'form': IniciarSesion(),
                    'error': 'Email y contraseña son requeridos.'
                })
        else:
            restaurante = Restaurante.objects.filter(email=email).first()
            cliente = Cliente.objects.filter(email=email).first()

            if restaurante and (check_password(password, restaurante.password) or password==restaurante.password):
                request.session['tipo']=True
                request.session['email'] = restaurante.email
                restaurante.last_login = timezone.now()
                restaurante.is_active = True
                restaurante.save()
                if 'registro' in request.session:
                    restaurante_id = request.session.get("restaurante")
                    if bool(request.session.get("registro")):
                        return redirect('registro_datos', id=restaurante_id)  # Redirigir al perfil
                else:
                    return redirect('perfil-restaurante')  # Redirigir al perfil
                # Intentar con el cliente
            elif cliente and (check_password(password, cliente.password) or password== cliente.password):
                request.session['tipo']=False
                request.session['email'] = cliente.email
                cliente.last_login = timezone.now()
                cliente.is_active = True
                cliente.save()
                if 'registro' in request.session:
                    restaurante_id = request.session.get("restaurante")
                    if bool(request.session.get("registro")):
                        total = request.session.get("total")
                        return redirect('pago', id=restaurante_id, total=total)  # Redirigir al pago
                else:
                    return redirect('perfil-cliente')  # Redirigir al perfil
            else:
                # Si el usuario no fue encontrado
                return render(request, 'usuario_sesion/login.html', {
                        'form': IniciarSesion(),
                        'error': 'Usuario no encontrado, revise su email o contraseña'
                })
def logout(request):
    email = request.session.get('email')
    if email:
        Restaurante.objects.filter(email=email).update(is_active=False)
        Cliente.objects.filter(email=email).update(is_active=False)
        # Cerrar la sesion
        valor_a_conservar = request.session.get('ubicacion')
             #vaciar todas las variables de sesión
        request.session.flush()

                # Restaurar la variable que deseas conservar
        request.session['ubicacion'] = valor_a_conservar
        return redirect('home') 

    return HttpResponse("No se logró cerrar la cuenta")

def registro_restaurante(request):
    session_keys = ['registro', 'nombre', 'identificacion', 'mail', 'telefono']
    for key in session_keys:
        request.session.pop(key, None)
    if request.method == 'GET':
        return render(request, 'user2/registro_restaurante.html', {
            'form': CreateNewRestauranteForm(),
        })
    elif request.method == 'POST':
        form = CreateNewRestauranteForm(request.POST)
        if form.is_valid():
            # chequear que las contraseñas coinciden
            if form.cleaned_data['password1'] == form.cleaned_data['password2']:
                try:
                    # crear el nuevo usuario restaurante
                    restaurante = Restaurante(
                        nombre=form.cleaned_data["nombre"],
                        rif=form.cleaned_data["rif"],
                        email=form.cleaned_data["email"],
                        telefono=form.cleaned_data["telefono"],
                        password=make_password(form.cleaned_data["password1"]),
                        username=form.cleaned_data["username"],
                    )
                    # hash de django con la contraseña
                    restaurante.is_active=True
                    restaurante.save()                    
                    request.session['email'] = restaurante.email
                    request.session['type']=True
                    if 'registro' in request.session:
                        restaurante=request.session.get("restaurante")
                        if bool(request.session.get("registro"))==True:
                            return redirect('registro_datos',id=restaurante)  # rederigir al perfil
                    else:
                        return redirect('perfil-restaurante')  # rederigir al perfil
                except Exception as e:
                    return render(request, 'user2/registro_restaurante.html', {
                        'form': form,
                        'error': f'El usuario ya existe, {e}',
                    })
            else:
                return render(request, 'user2/registro_restaurante.html', {
                    'form': form,
                    'error': 'Las contraseñas no coinciden'
                })
        else:
            return render(request, 'user2/registro_restaurante.html', {
                'form': form,
                'error': 'Por favor, corrige los errores en el formulario.'
            })

def registro_cliente(request):
    session_keys = ['registro', 'nombre', 'identificacion', 'mail', 'telefono']
    for key in session_keys:
        request.session.pop(key, None)

    if request.method == 'GET':
        return render(request, 'registro_cliente.html', {
            'form': CreateNewClientForm(),
        })
    elif request.method == 'POST':
        form = CreateNewClientForm(request.POST)
        if form.is_valid():
            try:
                cliente = Cliente(
                    nombre=form.cleaned_data["nombre"],
                    cedula=form.cleaned_data["cedula"],
                    email=form.cleaned_data["email"],
                    telefono=form.cleaned_data["telefono"],
                    username=form.cleaned_data["username"],
                    password=make_password(form.cleaned_data["password2"]),  # Hashear la contraseña
                    is_active=True
                )
                cliente.save()
                request.session['email'] = cliente.email
                request.session['type'] = False
                if 'registro' in request.session:
                    restaurante = request.session.get("restaurante")
                    if bool(request.session.get("registro")):
                        return redirect('registro_datos', id=restaurante)  # redirigir al perfil
                else:
                    return redirect('perfil-cliente')  # redirigir al perfil
            except Exception as e:
                messages.error(request, 'El usuario ya existe: {}'.format(e))
                return render(request, 'registro_cliente.html', {
                    'form': form,
                })
        else:
            print(form.errors)  # Imprimir errores de validación
            messages.error(request, 'Por favor, corrige los errores en el formulario.')
            return render(request, 'registro_cliente.html', {
                'form': form,
            })

def cuenta(request):
    mail = request.session.get('email')
    print(mail)
    cliente = Cliente.objects.filter(email=mail).first()
    if not mail:
        return render(request, 'usuario_sesion/login.html', {
            'form': IniciarSesion(),
            'error': 'Email o contraseña incorrecto'
        })


    elif cliente and cliente.is_active:
        form=CuentaCliente(instance=cliente)
        for field in form.fields.values(): 
            field.widget.attrs['readonly'] = True
        return render(request, 'perfil_cliente.html', {
            'nombre':cliente.nombre,
            'form':form,
        })

    return render(request, 'usuario_sesion/login.html', {
        'form': IniciarSesion(),
        'error': 'Email o contraseña incorrecto'
    })

def ModificarCuenta(request):#cliente
    mail = request.session.get('email')
    cliente = Cliente.objects.filter(email=mail).first()

    if request.method == 'GET':
        if cliente and cliente.is_active:
            form = CuentaCliente(instance=cliente)
            return render(request, 'editar_perfilUsuario.html', {
                'nombre': cliente.nombre,
                'form': form,
            })

    else:
        if cliente and cliente.is_active:
            form = CuentaCliente(request.POST, instance=cliente)
            if form.is_valid():
                try:
                    form.save()
                    return redirect('perfil-cliente')
                except ValueError:
                    return render(request, 'editar_perfilUsuario.html', {
                        'nombre': cliente.nombre,
                        'form': form,
                        'error': 'Error actualizando datos'
                    })
            else:
                return render(request, 'editar_perfilUsuario.html', {
                    'nombre': cliente.nombre,
                    'form': form,
                    'error': 'Por favor, corrige los errores en el formulario.'
                })

def NotificacionesView(request):
    mail=request.session.get('email')
    restaurante=Restaurante.objects.filter(email=mail).first()
    cliente=Cliente.objects.filter(email=mail).first()

    if restaurante:
        mail=restaurante.email
    elif cliente:
        mail=cliente.email
    pedido=PedidoModel.objects.filter(email=mail).all()
    for p in pedido:
        p=str(p.nro)
    reservacion=Reservacion_cliente.objects.filter(email=mail).all()
    return render(request,'notificaciones.html',{
            'pedidos': pedido,
            'reservacion': reservacion,
        })

def DetailView(request,nro):
    mail = request.session.get('email')
    if not mail:
        return render(request, 'usuario_sesion/login.html', {
            'form': IniciarSesion(),
            'error': 'Email o contraseña incorrecto'
        })
    else:
        if request.method=="GET":
            
            #nro inidca el pedido en la base de datos, cada uno tiene un numero diferente
            pedido=PedidoModel.objects.filter(nro=nro).first()

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
                comida = Menu.objects.filter(item=elegido, restaurante=pedido.id_nro).first()
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
            elif pedido.puntodeventa_active==True:
                pago=paypal
                text="Punto de venta"
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

            return render(request, 'detail.html',{
                'pedidos':pedido,
                'detalles':detalles_items,
                'subtotal': round(total, 2),
                'iva': round(iva, 2),
                'bolivares': round(bolivares,2),
                'pago':pago,
                'text':text,
                'diccionario': diccionario,
            })