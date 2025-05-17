# main/context_processors.py

def nav_links_processor(request):
    email = request.session.get('email')
    tipo=False
    if 'tipo' in request.session:
        tipo=request.session.get('tipo')
        tipo=int(tipo)
        tipo=bool(tipo)
    print('TIPO', tipo)
    if email:
        if tipo:
            nav_links = {
                'perfil_url': '/perfil-restaurante/',  # URL para el perfil de usuario
                'logout_url': '/logout/',  # URL para cerrar sesión
                'pedido_url': '/notifications/'
            }
        else:
             nav_links = {
                'perfil_url': '/perfil-cliente/',  # URL para el perfil de usuario
                'logout_url': '/logout/',  # URL para cerrar sesión
                'pedido_url': '/notifications/'
            }
    
    else:
        nav_links = {
            'login_url': '/login/'  # URL para iniciar sesión
        }
    return {'nav_links': nav_links}
