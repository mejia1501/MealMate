<div align="center">

# 🍽️ MealMate

### *Tu compañero perfecto para la experiencia gastronómica digital*

[![Python](https://img.shields.io/badge/Python-3.12.6-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.1.2-green?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![JavaScript](https://img.shields.io/badge/JavaScript-ES6-yellow?style=for-the-badge&logo=javascript&logoColor=white)](https://www.javascript.com/)
[![Leaflet](https://img.shields.io/badge/Leaflet-1.9.4-green?style=for-the-badge&logo=leaflet&logoColor=white)](https://leafletjs.com/)

[🚀 Demo](#) | [📖 Documentación](#documentación-técnica) | [💻 Instalación](#instalación-y-configuración)

</div>

---

## 🌟 ¿Qué es MealMate?

**MealMate** es una plataforma web moderna e innovadora que revoluciona la forma en que los restaurantes se conectan con sus clientes. Con una interfaz intuitiva y elegante, ofrecemos una experiencia gastronómica digital completa que combina tecnología de vanguardia con facilidad de uso.

### 💡 La Solución Definitiva para la Industria Alimentaria

En la era digital, los comensales buscan comodidad, rapidez y flexibilidad. MealMate responde a estas necesidades con una plataforma todo-en-uno que permite a los usuarios:

- 🚚 **Pedir delivery** con seguimiento en tiempo real
- 🏪 **Recoger pedidos** (Pick-up) en el momento perfecto
- 📅 **Reservar mesas** de forma instantánea
- 💳 **Pagar de múltiples formas** adaptadas al mercado local e internacional

---

## ✨ Características Principales

<table>
<tr>
<td width="50%">

### 🎯 Para Clientes

- **🔍 Búsqueda Inteligente**: Encuentra restaurantes y platillos fácilmente
- **🗺️ Mapas Interactivos**: Visualiza ubicaciones con Leaflet
- **⏰ Horarios Flexibles**: Agenda tus pedidos y reservas
- **💰 Múltiples Métodos de Pago**: 
  - Pago Móvil 📱
  - PayPal 💳
  - Zelle 💵
  - Efectivo 💸
  - Punto de Venta 🏧
- **📊 Seguimiento en Tiempo Real**: Monitorea tu pedido

</td>
<td width="50%">

### 🏪 Para Restaurantes

- **📋 Gestión de Menú**: Administra platillos e ingredientes
- **🪑 Control de Reservaciones**: Sistema de mesas inteligente
- **📦 Gestión de Pedidos**: Delivery y Pick-up unificados
- **💹 Conversión de Divisas**: Soporte multi-moneda
- **📈 Dashboard Administrativo**: Panel de control completo
- **🔐 Autenticación Segura**: Sistema robusto de usuarios

</td>
</tr>
</table>

---

## 🏗️ Arquitectura Técnica

MealMate está construido con una arquitectura moderna y escalable que garantiza rendimiento, seguridad y mantenibilidad.

### 🛠️ Stack Tecnológico

#### **Backend**
- **Framework**: Django 5.1.2 (Python Web Framework)
- **Lenguaje**: Python 3.12.6
- **API REST**: Django REST Framework
- **ORM**: Django ORM para gestión de base de datos
- **Geolocalización**: GeoPy para cálculos de distancia

#### **Frontend**
- **Estructura**: HTML5 semántico
- **Estilos**: CSS3 con diseño responsive
- **Interactividad**: JavaScript ES6
- **Mapas**: Leaflet 1.9.4 para visualización geográfica
- **UI/UX**: Interfaz limpia y minimalista

#### **Base de Datos**
- **SQLite**: Base de datos por defecto (desarrollo)
- **Modelos principales**:
  - Restaurantes y Menús
  - Pedidos (Delivery/Pick-up)
  - Reservaciones
  - Métodos de Pago
  - Usuarios y Autenticación

---

## 📦 Estructura del Proyecto

```
MealMate/
├── 📁 project_admin/      # Configuración principal de Django
│   ├── settings.py        # Configuraciones del proyecto
│   ├── urls.py            # Enrutamiento principal
│   └── wsgi.py            # WSGI para deployment
│
├── 📁 principal/          # App principal y home
│   ├── views.py           # Vistas principales
│   ├── templates/         # Plantillas HTML
│   └── static/            # CSS, JS e imágenes
│
├── 📁 usuario_sesion/     # Sistema de autenticación
│   ├── views.py           # Login y registro
│   └── templates/         # Plantillas de sesión
│
├── 📁 user_r/             # Gestión de restaurantes
│   ├── models.py          # Modelos de restaurante y menú
│   └── forms.py           # Formularios de administración
│
├── 📁 servicios/          # Reservaciones y servicios
│   ├── models.py          # Modelos de reservas
│   └── views.py           # Lógica de reservaciones
│
├── 📁 pedidos/            # Sistema de pedidos
│   ├── views.py           # Delivery y Pick-up
│   ├── forms.py           # Formularios de pedidos
│   └── templates/         # Plantillas de pedidos
│
└── 📄 manage.py           # CLI de Django
```

---

## 🚀 Instalación y Configuración

### Prerrequisitos

- Python 3.12.6 o superior
- pip (gestor de paquetes de Python)
- Git

### Pasos de Instalación

1. **Clonar el repositorio**
```bash
git clone https://github.com/mejia1501/MealMate.git
cd MealMate
```

2. **Crear entorno virtual**
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. **Instalar dependencias**
```bash
pip install django==5.1.2
pip install djangorestframework
pip install geopy
pip install pytz
```

4. **Configurar base de datos**
```bash
python manage.py makemigrations
python manage.py migrate
```

5. **Crear superusuario (opcional)**
```bash
python manage.py createsuperuser
```

6. **Ejecutar servidor de desarrollo**
```bash
python manage.py runserver
```

7. **Acceder a la aplicación**
```
Abre tu navegador en: http://127.0.0.1:8000/
```

---

## 🔧 Configuración Avanzada

### Variables de Entorno

Crea un archivo `.env` en la raíz del proyecto:

```env
SECRET_KEY=tu-clave-secreta-aqui
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

### Base de Datos en Producción

Para usar PostgreSQL en producción:

```bash
pip install psycopg2-binary
```

Actualiza `settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'mealmate_db',
        'USER': 'tu_usuario',
        'PASSWORD': 'tu_contraseña',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

---

## 🎨 Características Técnicas Destacadas

### 🗺️ Sistema de Geolocalización
- Integración con Leaflet para mapas interactivos
- Cálculo de distancias con GeoPy
- Visualización de ubicaciones de restaurantes

### 💳 Procesamiento de Pagos
- Soporte para pagos locales (Pago Móvil con bancos venezolanos)
- Integración con PayPal para pagos internacionales
- Sistema Zelle para transferencias
- Conversión automática de divisas (USD/Bs)

### 📅 Sistema de Reservaciones
- Gestión inteligente de mesas
- Control de horarios y disponibilidad
- Confirmación automática por email

### 🔐 Seguridad
- Autenticación robusta con Django Auth
- Protección CSRF
- Validación de formularios
- Sanitización de datos

---

## 📱 Responsive Design

MealMate está optimizado para funcionar perfectamente en:

- 📱 Móviles (iOS y Android)
- 💻 Tablets
- 🖥️ Desktop

---

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Si deseas mejorar MealMate:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

---

## 📄 Licencia

Este proyecto está bajo una licencia privada. Todos los derechos reservados.

---

## 👥 Equipo

Desarrollado con ❤️ por el equipo de MealMate

---

## 📞 Contacto y Soporte

¿Tienes preguntas o sugerencias? 

- 📧 Email: [Contacto](mailto:contacto@mealmate.com)
- 🐛 Issues: [GitHub Issues](https://github.com/mejia1501/MealMate/issues)
- 💬 Discusiones: [GitHub Discussions](https://github.com/mejia1501/MealMate/discussions)

---

<div align="center">

### 🌟 ¡Dale una estrella si te gusta este proyecto! ⭐

**MealMate** - *Conectando restaurantes con comensales, un clic a la vez* 🍽️

</div>
