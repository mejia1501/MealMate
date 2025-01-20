from django.shortcuts import render,redirect
from usuario_sesion.forms import IniciarSesion
from .forms import CuentaRestaurante,Items,PagoForm,ZelleForm,PaypalForm,AddIngredients
from .models import Restaurante,Menu,Ingredientes,Pago,Paypal,Zelle
from django.contrib import messages
from datetime import date
# Create your views here

#enviar datos a los perfiles
def cuenta(request):
    #obtencion de la variable de sesion email
    mail = request.session.get('email')
    if not mail:
        return render(request, 'usuario_sesion/login.html', {
            'form': IniciarSesion(),
            'error': 'Email o contraseña incorrecto'
        })

    restaurante = Restaurante.objects.filter(email=mail).first()
    request.session['restaurante']=restaurante.id
    if (restaurante and restaurante.is_active):

        form=CuentaRestaurante(instance=restaurante)

        for field in form.fields.values():#lee cada valor del form
            field.widget.attrs['readonly'] = True#readonly,solo mostrar
        if restaurante.direccion!="":
            coordenadas=restaurante.direccion.split('+')
        #Manejo de la fecha de fundación
        if restaurante.fundacion:
            date_fundacion = restaurante.fundacion.isoformat
        else:
            date_fundacion = None

        return render(request, 'perfil_restaurante.html', {
            'nombre':restaurante.nombre,
            'form':form,
            'latitud': str(coordenadas[0]) if restaurante.direccion!="" else False,
            'longitud': str(coordenadas[1]) if restaurante.direccion!="" else False,
            'date': date_fundacion if date_fundacion else False,
        })

    return render(request, 'usuario_sesion/login.html', {
        'form': IniciarSesion(),
        'error': 'Email o contraseña incorrecto'
    })

#modificar cuenta resturante
def ModificarCuenta(request):
    mail = request.session.get('email')
    restaurante=Restaurante.objects.filter(email=mail).first()

    #se obtienen los datos correspondientes al usuario loguado y se muestran en pantalla
    if request.method == 'GET':
        if restaurante and restaurante.is_active:
            # Verificar si la dirección no es None o vacía
            if restaurante.direccion:
                coordenadas = restaurante.direccion.split('+')

                # Asegurarse de que hay al menos dos coordenadas
                latitud = str(coordenadas[0])
                longitud = str(coordenadas[1])
            else:
                latitud = None
                longitud = None
            # Manejo de la fecha de fundación
            if restaurante.fundacion:
                date_fundacion = restaurante.fundacion.isoformat
            else:
                date_fundacion = None

            form = CuentaRestaurante(instance=restaurante)

            return render(request, 'editar_perfil.html', {
                'form': form,
                'latitud': latitud,
                'longitud': longitud,
                'date': date_fundacion if date_fundacion else False,
                'hoy': date.today().isoformat,
            })
#se modifican los datos del usuario logueado segun lo que envie con el formulario CuentaRestaurante
    elif request.method == 'POST':
        if restaurante and restaurante.is_active:
            form = CuentaRestaurante(request.POST, instance=restaurante)
            latitude = request.POST.get('latitude')
            longitude = request.POST.get('longitude')
            fundacion = request.POST.get('fundacion')
            #verificar que el formulario no tenga errores
            if form.is_valid() and latitude and  longitude and fundacion:
                try:
                    restaurante.direccion= f"{latitude}+{longitude}"
                    restaurante.fundacion=fundacion
                    restaurante.save()
                    form.save()#guardar formulario
                    return redirect('perfil-restaurante')#rederigir al usuario a su perfil luego de modificarlo
                except ValueError:
                    return render(request, 'editar_perfil.html', {
                        'nombre': restaurante.nombre,
                        'form': form,
                        'error': 'Error actualizando datos'
                    })
            else:
                return render(request, 'editar_perfil.html', {
                    'nombre': restaurante.nombre,
                    'form': form,
                    'error': 'Por favor, corrige los errores en el formulario.'
                })
            
#creacion del menu con el formulario item            
def CrearMenu(request):
    mail = request.session.get('email')
    if not mail:

        return render(request, 'usuario_sesion/login.html', {
            'form': IniciarSesion(),
            'error': 'Email o contraseña incorrecto'
        })
    if request.method == 'GET':
        #entorno=1=crear, entorno=0=modificar
        request.session['entorno']=0
        return render(request, 'crear_comida.html', {
            'form': Items(),
            'code':'0',

        })
    else:
        form = Items(request.POST)
        if form.is_valid():
            try:
                print("INGREDIENTES",form.cleaned_data['ingredientes'])
                #se guardan los datos del formulairo en el modelo Menu
                restaurant = Restaurante.objects.filter(email=mail).first()
                codigo=','.join([str(ingrediente) for ingrediente in form.cleaned_data['ingredientes']])
                nuevo_menu = Menu(
                    restaurante=restaurant,
                    comida=form.cleaned_data["plato"],
                    precios=form.cleaned_data["precio"],
                    codigo=codigo,
                )
                nuevo_menu.save()
                return redirect("menu")
            except Exception as e:
                return render(request, 'crear_comida.html', {
                    'form': form,
                    'error': f'Error al guardar los datos: {str(e)}'
                })
        else:
            return render(request, 'crear_comida.html', {
                'form': form,
                'error': 'Por favor, corrige los errores en el formulario.'
            })

def MostrarMenu(request):
    if 'entorno' in request.session:
        del request.session['entorno']
    mail = request.session.get('email')
    if not mail:
        return render(request, 'usuario_sesion/login.html', {
            'form': IniciarSesion(),
            'error': 'Email o contraseña incorrecto'
        })

    try:
        # Verificar si se encuentra el restaurante
        restaurant = Restaurante.objects.filter(email=mail).first()
        if not restaurant:
            return render(request, 'menu.html', {
                'error': 'Restaurante no encontrado.',
            })
        
        # Filtrar los menús que pertenecen a este restaurante
        menus = Menu.objects.filter(restaurante=restaurant.id).all()
        
        if not menus.exists():
            return render(request, 'menu.html', {
                'nombre': restaurant.nombre,
                'error': "No se encontró el menú.",
            })

        texto = {}
        lista = []
        #transformar los codigo en string segun el modelo ingredientes
        for item in menus:
            #vaciar las variables luego de cada iteracion
            lista.clear()
            ingredient = ""
            #guardar los codigos de ingredientes en una lista
            lista = item.codigo.split(',')
            for codigo in lista:
                #se guarda en la varible consulta la coicidencia del ingrediente en el modelo Ingredientes
                consulta = Ingredientes.objects.filter(codigo=codigo).first()
                if consulta:
                    #si hay una cocincidencia se concatena en la variable string
                    ingredient += str(consulta) + ","
            #Eliminar todas las comas al final de la cadena:
            while ingredient.endswith(","): 
                ingredient = ingredient[:-1]
            #guardar los datos en la biblioteca texto
            texto.update({item.item: ingredient})
            print(menus)
      #envio de datos al menu.html
        return render(request, 'menu.html', {
            'menus': menus,
            'ingredients': texto, 
            'nombre': restaurant.nombre,
        })
#control de errores
    except Exception as e:
        return render(request, 'menu.html', {
            'nombre': restaurant.nombre if restaurant else "Desconocido",
            'error': f"Error al traer datos: {str(e)}",
        })

#se modifica el item que el usuario selecciono
def ModificarMenu(request,item):
    mail = request.session.get('email')
    
    if not mail:
        return render(request, 'usuario_sesion/login.html', {
            'form': IniciarSesion(),
            'error': 'Email o contraseña incorrecto'
        }) 

    restaurante = Restaurante.objects.filter(email=mail).first()
    if not restaurante:
        return render(request, 'menu.html', {'error': 'Restaurante no encontrado.'})
#envio de datos a la pagian editar menu con la estructura del form Menu y con informacion inicial proveniente del modelo Menu
    comida1 = Menu.objects.filter(item=item,restaurante=restaurante.id).first()
    if not comida1:
            return render(request, 'menu.html', {'error': 'Menú no encontrado.'})
        
    codigos = comida1.codigo.split(',')
        # Convertir cada elemento de la lista a un número
    codigos_numericos = [int(codigo) for codigo in codigos]
    form = Items(initial={ 
            'plato': comida1.comida, 
            'precio': comida1.precios,
            'ingredientes': codigos_numericos,
            })
    if request.method == "GET":
        #entorno=1=crear, entorno=0=modificar
        request.session['entorno']=0
        return render(request, 'editar_menu.html', {'form': form,'code':item})

    if request.method == "POST":
        try:
            comida = Menu.objects.filter(item=int(item),restaurante=restaurante.id).first()
            if not comida:
                return render(request, 'menu.html', {'error': 'Comida no encontrado.'})
            
            form2 = Items(request.POST)
            if form2.is_valid():
                comida.comida = form2.cleaned_data['plato']
                comida.precios = form2.cleaned_data['precio']
                ingredientes = form2.cleaned_data['ingredientes']
                print("COMIDA OBJECCT ", comida)
                print("INGREDIENTES ",ingredientes)
                # Convertir explícitamente cada código de ingrediente a una cadena
                comida.codigo = ",".join([str(ingrediente) for ingrediente in ingredientes])
                comida.save()
                return redirect('menu')
            else:
                return render(request, 'editar_menu.html', {'form': form, 'error': 'Formulario no válido','code':comida1.item})

        except Exception as e:
            return render(request, 'editar_menu.html', {'form': form, 'error': f'Error al guardar los cambios: {str(e)}','code':comida1.item})

    return render(request, 'menu.html', {'error': 'Método no permitido'})

def DeleteDish(request,item):
    mail = request.session.get('email')
    if not mail:
        return render(request, 'usuario_sesion/login.html', {
            'form': IniciarSesion(),
            'error': 'Email o contraseña incorrecto'
        })
    comida = Menu.objects.filter(item=item).first()
    if not comida:
        return render(request, 'delete_dish.html', {'error': 'Plato no encontrado.'})
    else:
        if request.method == "POST":
            try:
                comida.delete()
                messages.success(request, 'Plato eliminado con éxito.')
                return redirect('menu')
                
            except Exception as e:
                return render(request, 'menu.html', {'error': f'Error al guardar los cambios: {str(e)}'})
        else:
            return render(request,'delete_dish.html',{'name':comida.comida,'item':item})

def NuevoIngrediente(request,nro):
    mail = request.session.get('email')
    if not mail:
        return render(request, 'usuario_sesion/login.html', {
            'form': IniciarSesion(),
            'error': 'Email o contraseña incorrecto'
        })
    
    restaurante = Restaurante.objects.filter(email=mail).first()
    
    if request.method == "GET":
        return render(request, 'add_ingredient.html', {
            'form': AddIngredients(),
            'item': int(nro),
        })
    else:
        form = AddIngredients(request.POST)
        if form.is_valid():  # Asegúrate de validar el formulario
            review=Ingredientes.objects.filter(ingrediente=form.cleaned_data["ingrediente"].lower())
            if review:
                return render(request, 'add_ingredient.html', {
                'error': "Ingrediente ya creado",
                'form': form,
                'name': restaurante.nombre,
            })
            else:
                new = Ingredientes(
                    ingrediente=form.cleaned_data["ingrediente"],
                )
                new.save()
                nro=int(nro)
                #entorno=1=crear, entorno=0=modificar
                if int(request.session.get('entorno'))==1:
                    return redirect('crear_menu')
                else:
                    nro=str(nro)
                    return redirect('editar_menu',item=nro)
        else:
            # Si el formulario no es válido, puedes volver a renderizar la página con errores
            return render(request, 'add_ingredient.html', {
                'form': form,
                'name': restaurante.nombre,
            })
        
def PagoNacional(request):
    # Get the email from the session
    mail = request.session.get('email')

    # Check if the user is logged in
    if not mail:
        return render(request, 'usuario_sesion/login.html', {
            'form': IniciarSesion(),
            'error': 'Email o contraseña incorrecto'
        })

    # Get the restaurant instance
    restaurant = Restaurante.objects.filter(email=mail).first()

    # Handle GET requests
    if request.method == 'GET':
        # Get the existing national payment instance
        nacional = Pago.objects.filter(restaurante=restaurant.id).first()

        # Initialize the form with existing data if available
        if nacional:
            form = PagoForm(initial={
                'efectivo': nacional.efectivo_active,
                'punto_venta':nacional.punto_active,
                'phone': nacional.telefono_pm,
                'banco': nacional.banco,
            })
        else:
            form = PagoForm()

        return render(request, 'pago_nacional.html', {
            'form': form,
            'nombre':restaurant.nombre,
        })

    # Handle POST requests
    elif request.method == 'POST':
        form = PagoForm(request.POST)

        # Validate the form
        if form.is_valid():
            try:
                # Get the existing national payment instance
                nacional = Pago.objects.filter(restaurante=restaurant.id).first()

                # Update the existing instance or create a new one
                if nacional:
                    nacional.banco = form.cleaned_data["banco"]
                    nacional.pagomovil_active = True
                    nacional.efectivo_active = form.cleaned_data["efectivo"]
                    nacional.telefono_pm = form.cleaned_data["phone"]
                    nacional.punto_active= form.cleaned_data['punto_venta']
                    nacional.save()
                else:
                    Pago.objects.create(
                        restaurante=restaurant,
                        banco=form.cleaned_data["banco"],
                        pagomovil_active=True,
                        punto_active=form.cleaned_data['punto_venta'],
                        efectivo_active=form.cleaned_data["efectivo"],
                        telefono_pm=form.cleaned_data["phone"]
                    )

                return redirect("pago_nacional")
            except Exception as e:
                return render(request, 'pago_nacional.html', {
                    'form': form,
                    'nombre':restaurant.nombre,
                    'error': f'Error al guardar los datos: {str(e)}'
                })
        else:
            return render(request, 'pago_nacional.html', {
                'form': form,
                'nombre':restaurant.nombre,
                'error': 'Por favor, corrige los errores en el formulario.'
            })
        
def PaypalView(request):
    mail = request.session.get('email')
    restaurante = Restaurante.objects.filter(email=mail).first()

    if request.method == 'GET':
        if restaurante and restaurante.is_active:
            # Busca una instancia existente de Paypal o crea una nueva si no existe
            paypal_instance = Paypal.objects.filter(restaurante=restaurante).first()
            if not paypal_instance:
                paypal_instance = Paypal(restaurante=restaurante)
            form = PaypalForm(instance=paypal_instance)
            return render(request, 'paypal.html', {'form': form,'nombre':restaurante.nombre})

    elif request.method == 'POST':
        if restaurante and restaurante.is_active:
            paypal_instance = Paypal.objects.filter(restaurante=restaurante).first()
            if not paypal_instance:
                paypal_instance = Paypal(restaurante=restaurante)
            form = PaypalForm(request.POST, instance=paypal_instance)
            if form.is_valid():
                try:
                    new = form.save(commit=False)  # No guarda todavía en la base de datos
                    new.paypal_active = True  # Actualiza el campo paypal_active
                    new.save()  # Guarda la instancia con el cambio realizado
                    return redirect('paypal')
                except ValueError:
                    return render(request, 'paypal.html', {
                        'form': form,
                        'error': 'Error actualizando datos'
                    })
            else:
                return render(request, 'paypal.html', {
                    'form': form,
                    'error': 'Por favor, corrige los errores en el formulario.'
                })
 
def ZelleView(request):
    mail = request.session.get('email')
    restaurante = Restaurante.objects.filter(email=mail).first()

    if request.method == 'GET':
        if restaurante and restaurante.is_active:
            # Busca una instancia existente de Zelle o crea una nueva si no existe
            zelle_instance = Zelle.objects.filter(restaurante=restaurante).first()
            if not zelle_instance:
                zelle_instance = Zelle(restaurante=restaurante)
            form = ZelleForm(instance=zelle_instance)
            return render(request, 'zelle.html', {'form': form,'nombre':restaurante.nombre})

    elif request.method == 'POST':
        if restaurante and restaurante.is_active:
            zelle_instance = Zelle.objects.filter(restaurante=restaurante).first()
            if not zelle_instance:
                zelle_instance = Zelle(restaurante=restaurante)
            form = ZelleForm(request.POST, instance=zelle_instance)
            if form.is_valid():
                try:
                    new = form.save(commit=False)  # No guarda todavía en la base de datos
                    new.zelle_active = True  # Actualiza el campo zelle_active
                    new.save()  # Guarda la instancia con el cambio realizado
                    return redirect('zelle')
                except ValueError:
                    return render(request, 'zelle.html', {
                        'form': form,
                        'error': 'Error actualizando datos'
                    })
            else:
                return render(request, 'zelle.html', {
                    'form': form,
                    'error': 'Por favor, corrige los errores en el formulario.'
                })
            

