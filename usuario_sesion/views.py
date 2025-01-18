from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import CreateNewRestauranteForm, IniciarSesion, CreateNewClientForm, CuentaCliente
from user_r.models import Restaurante
from .models import Cliente
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

# Define el tiempo límite en días para borrar las variables de sesión
TIEMPO_LIMITE = 20  # 20 días

def iniciar_sesion(request):
    # Establecer el timestamp si no existe
    if 'timestamp' not in request.session:
        request.session['timestamp'] = timezone.now().isoformat()  # Almacenar como cadena

    # Convertir el timestamp de nuevo a datetime
    timestamp = timezone.datetime.fromisoformat(request.session['timestamp'])

    # Verificar si el tiempo ha excedido el límite
    tiempo_transcurrido = timezone.now() - timestamp
    if tiempo_transcurrido > timedelta(days=TIEMPO_LIMITE):
        # Limpiar todas las variables de sesión
        valor_a_conservar = request.session.get('ubicacion')
        
        # Vaciar todas las variables de sesión
        request.session.flush()

        # Restaurar la variable que deseas conservar
        if valor_a_conservar is not None:
            request.session['ubicacion'] = valor_a_conservar
        
        # Opcional: establecer un nuevo timestamp
        request.session['timestamp'] = timezone.now().isoformat()  # Almacenar como cadena

    if request.method == 'GET':
        return render(request, 'usuario_sesion/login.html', {
            'form': IniciarSesion()
        })
    else:
        email = request.POST['email']
        password = request.POST['password']

        if not email or not password:
            return render(request, 'usuario_sesion/login.html', {
                'form': IniciarSesion(),
                'error': 'Email y contraseña son requeridos.'
            })
    
        restaurante = Restaurante.objects.filter(email=email, password1=password, password2=password).first()
        if restaurante:
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
        cliente = Cliente.objects.filter(email=email, password=password).first()
        if cliente:
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

        # Si el usuario no fue encontrado
        return render(request, 'usuario_sesion/login.html', {
            'form': IniciarSesion(),
            'error': 'Email o contraseña incorrecto'
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
    if request.method == 'GET':
        return render(request, 'user2/registro_restaurante.html', {
            'form': CreateNewRestauranteForm(),
        })
    else:
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
                        password1=form.cleaned_data["password1"],
                        password2=form.cleaned_data["password2"],
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
    if request.method == 'GET':
        return render(request, 'registro_cliente.html', {
            'form': CreateNewClientForm(),
        })
    else:
        form = CreateNewClientForm(request.POST)
        if form.is_valid() :  # Asegúrate de validar el formulario
            if form.cleaned_data['password1'] == form.cleaned_data['password2']:
                try:
                    cliente = Cliente(
                        nombre=form.cleaned_data["nombre"],
                        cedula=form.cleaned_data["cedula"],
                        email=form.cleaned_data["email"],
                        telefono=form.cleaned_data["telefono"],
                        username=form.cleaned_data["username"],
                        password1=form.cleaned_data["password1"],
                        password2=form.cleaned_data["password2"],
                    )
                    cliente.is_active = True  
                    cliente.save()
                    request.session['email'] = cliente.email
                    request.session['type']=False
                    if 'registro' in request.session:
                        restaurante=request.session.get("restaurante")
                        if bool(request.session.get("registro"))==True:
                            return redirect('registro_datos',id=restaurante)  # rederigir al perfil
                    else:
                        return redirect('perfil-cliente')  # rederigir al perfil
                except Exception as e:
                    messages.error(request, 'El usuario ya existe: {}'.format(e))
                    return render(request, 'registro_cliente.html', {
                        'form': form,
                    })
            else:
                messages.error(request, 'Las contraseñas no coinciden')
        else:
            # Manejar errores de validación
            messages.error(request, 'Por favor, corrige los errores en el formulario.')
            return render(request, 'registro_cliente.html', {\
                'form': form,
            })

def cuenta(request):
    mail = request.session.get('email')

    if not mail:
        return render(request, 'usuario_sesion/login.html', {
            'form': IniciarSesion(),
            'error': 'Email o contraseña incorrecto'
        })

    cliente = Cliente.objects.filter(email=mail).first()
    if cliente and cliente.is_active:
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

