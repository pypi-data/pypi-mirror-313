import os
import ast
from django.core.management.base import BaseCommand
from django.core.management import call_command
from services.authentication import auth

class DjangoProjectManager:
    def __init__(self, app_name, project_name):
        self.app_name = app_name
        self.project_name = project_name

    def create_app(self):
        """
        Crea una aplicación de Django con el nombre especificado si no existe.
        """
        app_name = self.app_name
        if not os.path.exists(app_name):
            print(f"Creando la aplicación '{app_name}'...")
            call_command('startapp', app_name)
            if os.path.exists(app_name):
                print(f"La aplicación '{app_name}' fue creada exitosamente.")
            else:
                print(f"Error: No se pudo crear la aplicación '{app_name}'.")
        else:
            print(f"La aplicación '{app_name}' ya existe.")
    
    def installed_app(self):
        """
        Agrega la aplicación al archivo settings.py en la lista INSTALLED_APPS
        si no está ya presente. Asegura que se mantenga el formato adecuado.
        """
        settings_path = os.path.join(self.project_name, 'settings.py')

        # Leer el archivo settings.py
        with open(settings_path, 'r') as file:
            settings_content = file.read()

        # Comprobar si la aplicación ya está en INSTALLED_APPS
        if f"'{self.app_name}'" not in settings_content:
            # Buscar la línea donde está la lista INSTALLED_APPS
            installed_apps_start = settings_content.find("INSTALLED_APPS = [")
            installed_apps_end = settings_content.find("]", installed_apps_start) + 1

            # Extraer la lista INSTALLED_APPS
            installed_apps_content = settings_content[installed_apps_start:installed_apps_end]

            # Comprobar si la aplicación no está ya en INSTALLED_APPS
            if f"'{self.app_name}'" not in installed_apps_content:
                # Insertar la aplicación dentro de la lista
                new_installed_apps = installed_apps_content[:-1] + f"    '{self.app_name}',\n]"

                # Reemplazar el bloque INSTALLED_APPS con la nueva lista
                new_settings_content = settings_content[:installed_apps_start] + new_installed_apps + settings_content[installed_apps_end:]

                # Escribir los cambios de vuelta en settings.py
                with open(settings_path, 'w') as file:
                    file.write(new_settings_content)

                print(f"'{self.app_name}' fue agregado a INSTALLED_APPS.")
            else:
                print(f"'{self.app_name}' ya está en INSTALLED_APPS.")
        else:
            print(f"'{self.app_name}' ya está en INSTALLED_APPS.")
        
    def create_urls(self, stdout):
        """
        Modifica el archivo 'urls.py' del proyecto principal para agregar rutas si no están presentes.
        Si el archivo no existe, lo crea con un contenido básico.
        """
        project_urls_path = os.path.join(self.project_name, 'urls.py')

        if not os.path.exists(project_urls_path):
            stdout.write(f"Creando el archivo '{project_urls_path}'...")
            with open(project_urls_path, 'w') as f:
                f.write("""from django.contrib import admin
from django.urls import path, include  # Asegúrate de incluir include

urlpatterns = [
path('admin/', admin.site.urls),
path('', include('home.urls'))
    # Añade tus rutas aquí
]
    """)
        else:
            # Leer el contenido actual del archivo
            stdout.write(f"El archivo '{project_urls_path}' ya existe. Verificando contenido...\n")
            with open(project_urls_path, 'r') as f:
                urls_content = f.read()

            updated = False

            # Verificar si la ruta de 'Home.urls' está en 'urlpatterns'
            if "include('Home.urls')" not in urls_content:
                stdout.write("Agregando ruta para 'home.urls'.\n")
                
                # Agregar importación de 'include'
                urls_content = urls_content.replace(
                    "from django.urls import path",
                    "from django.urls import path, include"
                )
                
                # Agregar 'Home.urls' a 'urlpatterns'
                if "urlpatterns = [" in urls_content:
                    urls_content = urls_content.replace(
                        "urlpatterns = [",
                        "urlpatterns = [\n    path('admin/', admin.site.urls),\n    path('', include('Home.urls')),\n"
                    )
                updated = True

            # Escribir los cambios si se modificó algo
            if updated:
                with open(project_urls_path, 'w') as f:
                    f.write(urls_content)
                stdout.write(f"El archivo '{project_urls_path}' fue actualizado.\n")
            else:
                stdout.write(f"No fue necesario realizar cambios en '{project_urls_path}'.\n")

    def creation_auth(self, stdout):
        services_dir = os.path.join(self.app_name, 'services')
        authentication_dir = os.path.join(services_dir, 'authentication')
        os.makedirs(authentication_dir, exist_ok=True)

        # Ruta para el nuevo archivo a crear
        authentication_path = os.path.join(authentication_dir, 'authentication.py')

        # Usar el atributo __file__ del módulo 'auth' para obtener la ruta del archivo fuente
        auth_source_path = os.path.abspath(auth.__file__)

        if not os.path.exists(auth_source_path):
            stdout.write(f"El archivo fuente '{auth_source_path}' no existe. Verifica la instalación del paquete.")
            return

        if not os.path.exists(authentication_path):
            stdout.write(f"Creando el archivo '{authentication_path}'...")

            # Leer el contenido de 'auth.py' del paquete
            try:
                with open(auth_source_path, 'r') as source_file:
                    auth_code = source_file.read()

                # Escribir el contenido en el nuevo archivo 'authentication.py'
                with open(authentication_path, 'w') as dest_file:
                    dest_file.write(auth_code)

                stdout.write(f"El archivo '{authentication_path}' fue creado y el código fue copiado.")
            except Exception as e:
                stdout.write(f"Error al copiar el archivo: {e}")
        else:
            stdout.write(f"El archivo '{authentication_path}' ya existe.")

    def create_views_urls(self, stdout):
        home_dir = 'Home'  # Nombre de la aplicación Home
        views_path = os.path.join(home_dir, 'views.py')
        urls_path = os.path.join(home_dir, 'urls.py')

        # Crear el directorio de la aplicación Home si no existe
        if not os.path.exists(home_dir):
            os.makedirs(home_dir)  # Crear el directorio para la aplicación Home
            stdout.write(f"Directorio '{home_dir}' creado.\n")
        else:
            stdout.write(f"El directorio '{home_dir}' ya existe.\n")

        # Sobrescribir o crear el archivo views.py
        views_code = '''from django.shortcuts import render
from Home.services.authentication import Authentication

def home(request):
    return render(request, 'home.html')

def signup(request):
    return Authentication.get_signup(request)

def signout(request):
    return Authentication.get_signout(request)

def signing(request):
    return Authentication.get_signing(request)

def logged(request):
    return Authentication.get_logged(request)
        '''
        with open(views_path, 'w') as views_file:  # Abrir en modo escritura siempre
            views_file.write(views_code)
        stdout.write(f"El archivo '{views_path}' ha sido creado o sobrescrito.\n")

        # Verificar si urls.py existe y crearlo si no existe
        if not os.path.exists(urls_path):
            urls_code = '''from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name='home'),
    path("signup", views.signup, name='signup'),
    path("login", views.signing, name='login'),
    path("logout", views.signout, name='logout'),
    path("logged", views.logged, name='logged'),
]
        '''
            with open(urls_path, 'w') as urls_file:
                urls_file.write(urls_code)
            stdout.write(f"El archivo '{urls_path}' ha sido creado.\n")
        else:
            stdout.write(f"El archivo '{urls_path}' ya existe.\n")


























