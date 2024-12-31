from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import CreateNewRestaurante,IniciarSesion,CreateNewCliente,CuentaCliente
from user_r.models import Restaurante
from .models import Cliente
from django.utils import timezone

# Create your views here.
def iniciar_sesion(request):
    if request.method == 'GET':
        return render(request, 'usuario_sesion/login.html', {
            'form': IniciarSesion()
        })
    
    email = request.POST['email']
    password = request.POST['password']

    if not email or not password:
        return render(request, 'login.html', {
            'form': IniciarSesion(),
            'error': 'Email y contraseña son requeridos.'
        })
    restaurante = Restaurante.objects.filter(email=email, password=password).first()
    if restaurante:
        request.session['email'] = restaurante.email
        request.session['type']=True
        restaurante.last_login = timezone.now()
        restaurante.is_active=True
        restaurante.save()
        return redirect('perfil-restaurante')  # rederigir al perfil
    # intentar con el cliente
    cliente = Cliente.objects.filter(email=email, password=password).first()
    if cliente:
        request.session['email'] = cliente.email
        request.session['type']=False
        cliente.last_login = timezone.now()
        cliente.is_active=True
        cliente.save()
        return redirect('perfil-cliente')  # rederigir a perfil

    # Si el usuario no fue encontradp
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
        request.session.flush()#vaciar la variable de sesion
        return redirect('home') 

    return HttpResponse("No se logró cerrar la cuenta")

def registro_restaurante(request):
    if request.method == 'GET':
        return render(request, 'user2/registro_restaurante.html', {
            'form': CreateNewRestaurante()
        })
    else:
        form = CreateNewRestaurante(request.POST)
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
                        fundacion=form.cleaned_data["fundacion"],
                        logo=form.cleaned_data["logo"],
                        password=form.cleaned_data["password1"]
                    )
                    # hash de django con la contraseña
                    restaurante.is_active=True
                    restaurante.save()                    
                    request.session['email'] = restaurante.email
                    request.session['type']=True
                    return redirect("perfil-restaurante")
                except:
                    return render(request, 'user2/registro_restaurante.html', {
                        'form': form,
                        'error': 'El usuario ya existe'
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
            'form': CreateNewCliente()
        })
    else:
        form = CreateNewCliente(request.POST)
        if form.is_valid():  # Asegúrate de validar el formulario
            if form.cleaned_data['password1'] == form.cleaned_data['password2']:
                try:
                    cliente = Cliente(
                        nombre=form.cleaned_data["nombre"],
                        cedula=form.cleaned_data["cedula"],
                        email=form.cleaned_data["email"],
                        telefono=form.cleaned_data["telefono"],
                        password=form.cleaned_data["password1"]
                    )
                    cliente.is_active = True  
                    cliente.save()
                    request.session['email'] = cliente.email
                    request.session['type']=False
                    return redirect("perfil-cliente")
                except:
                    return render(request, 'registro_cliente.html', {
                        'form': form,
                        'error': 'El usuario ya existe'
                    })
            else:
                return render(request, 'registro_cliente.html', {
                    'form': form,
                    'error': 'Las contraseñas no coinciden'
                })
        else:
            return render(request, 'registro_cliente.html', {
                'form': form,
                'error': 'Por favor, corrige los errores en el formulario.'
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

