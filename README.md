# 🎯 Portafolio Personal

Portafolio personal desarrollado con Django para mostrar habilidades, experiencia y proyectos como Full Stack Developer (Python/Django · React) e Ingeniero Industrial. Incluye secciones de información personal, habilidades técnicas, currículum, contacto y certificaciones. Está construido con una arquitectura basada en principios SOLID para mantener el código limpio y escalable.

## Enlace de Portfolio
https://portafolio-propio.onrender.com

## 🚀 Tecnologías Utilizadas

- **Backend**: Django 6.0
- **API**: Django Rest Framework (DRF) 3.17.1
- **Autenticación**: Django REST Framework Simple JWT
- **Frontend**: HTML y CSS propio (sistema de diseño hecho a mano, sin framework ni build)
- **Base de Datos**: PostgreSQL o SQLite
- **Almacenamiento de medios**: Cloudinary
- **Despliegue**: Gunicorn, WhiteNoise
- **Otros**: Django Environ, Pillow, django-browser-reload

## ✨ Características

### Páginas Web
- **Inicio**: Página de bienvenida con diseño responsivo
- **Perfil**: Información personal del desarrollador
- **Acerca de mí**: Formación académica y habilidades técnicas
- **Currículum**: Descripción profesional detallada
- **Contacto**: Información de contacto
- **Proyectos**: Lista de proyectos con paginación
- **Certificaciones**: Sección dinámica para mostrar certificaciones gestionadas desde el backend

### Gestión de contenido
- **Modelo `Project`**: Administra proyectos con título, descripción, imagen Cloudinary y enlace
- **Modelo `Certification`**: Administra certificaciones con título, emisor, fecha, descripción y enlace de credencial
- **Admin personalizado**: Panel de administración disponible en `/config/`

### Internacionalización
- Soporte para **Español** e **Inglés**
- Cambio de idioma en el sitio por botón de navegación

### Arquitectura
- Implementación de principios SOLID (Single Responsibility, Open/Closed, Dependency Inversion, etc.)
- Servicios separados para lógica de negocio
- Vistas basadas en clases reutilizables
- Serializers preparados para API REST
- Soporte de recarga en caliente durante desarrollo con `django-browser-reload`

### API REST
- `GET /api/projects/` y `GET /api/certifications/` (solo lectura, paginados)
- Autenticación JWT: `POST /api/auth/token/` y `POST /api/auth/token/refresh/`
- Navegable en el navegador cuando `DEBUG=True`

## 🔧 Instalación

### Prerrequisitos
- Python 3.8+
- PostgreSQL (opcional, SQLite por defecto)

### Pasos

1. **Clona el repositorio:**
   ```bash
   git clone https://github.com/alejcuevas97/PORTAFOLIO_PROPIO.git
   cd Portafolio
   ```

2. **Crea entorno virtual:**
   ```bash
   python -m venv env
   env\Scripts\activate  # Windows
   source env/bin/activate  # Linux/Mac
   ```

3. **Instala dependencias de Python:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configura variables de entorno (.env):**
   Copia `.env.example` a `.env` en la raíz del proyecto y ajústalo. Todas las
   variables tienen valores por defecto para desarrollo local:
   - Sin `DATABASE_URL` → usa SQLite (`db.sqlite3`).
   - Sin credenciales `CLOUDINARY_*` → los archivos subidos se guardan en disco local.

   ```env
   DEBUG=True
   SECRET_KEY=tu_clave_secreta_aqui
   # DATABASE_URL=postgresql://usuario:clave@host:5432/basedatos
   # DATABASE_REQUIRE_SSL=True
   # CLOUDINARY_CLOUD_NAME=tu_cloud_name
   # CLOUDINARY_API_KEY=tu_api_key
   # CLOUDINARY_API_SECRET=tu_api_secret
   ```

6. **Ejecuta migraciones:**
   ```bash
   python manage.py migrate
   ```

7. **Crea superusuario (opcional):**
   ```bash
   python manage.py createsuperuser
   ```

8. **Recopila archivos estáticos:**
   ```bash
   python manage.py collectstatic --noinput
   ```

9. **Ejecuta el servidor:**
   ```bash
   python manage.py runserver
   ```
   Accede a http://localhost:8000

## 📁 Estructura del Proyecto

```
Portafolio/
├── Portafolio/          # Configuración principal de Django
│   ├── settings.py      # Configuraciones del proyecto
│   ├── urls.py          # Rutas principales
│   ├── views.py         # Vistas de páginas públicas
│   └── serializers.py   # Serializers para API
├── porfolio/            # App de portafolio
│   ├── models.py        # Modelo Project y validaciones
│   ├── views.py         # Lógica de proyectos y vistas de lista
│   ├── forms.py         # Formularios para el frontend
│   └── services.py      # Servicios de negocio
├── certificado/         # App de certificaciones
│   ├── models.py        # Modelo Certification
│   ├── views.py         # Vista de lista de certificaciones
│   ├── admin.py         # Registro en admin
│   └── urls.py          # Ruta de certificaciones
├── templates/           # Plantillas HTML
├── static/              # Archivos estáticos
├── media/               # Archivos multimedia
└── requirements.txt     # Dependencias Python
```

## 🚀 Uso

- Abrir la página principal en `/`
- Ver proyectos en `/proyectos/`
- Ver certificaciones en `/certificaciones/`
- Cambiar idioma con los botones `ES`/`EN` en la navegación
- Acceder al panel administrativo en `/config/`
- Consumir la API en `/api/projects/` y `/api/certifications/`
- Agregar proyectos y certificaciones desde el backend admin

## 🤝 Contribución

Si deseas contribuir al proyecto:

1. Haz un fork del repositorio
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Haz commit de tus cambios (`git commit -am 'Agrega nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia ISC.

## 📞 Contacto

- **Autor**: Alejandro Cuevas Gonzalez
- **GitHub**: [alejcuevas97](https://github.com/alejcuevas97)
- **Repositorio**: [PORTAFOLIO_PROPIO](https://github.com/alejcuevas97/PORTAFOLIO_PROPIO)
