import os
from django.core.management.base import BaseCommand
from services.authenticator_configurator import DjangoProjectManager

class Command(BaseCommand):
    help = 'Crea una aplicación llamada Home, estructura de carpetas y configura urls automáticamente en el proyecto especificado'

    def handle(self, *args, **kwargs):
        # Nombre de la aplicación a crear
        app_name = "Home"

        # definiendoerrores
        def write_file(file_path, content):
            try:
                with open(file_path, 'w') as file:
                    file.write(content)
                print(f"Archivo escrito correctamente: {file_path}")
            except Exception as e:
                print(f"Error al escribir el archivo {file_path}: {e}")

        # Paso 1: Solicitar el nombre de la aplicación principal al usuario
        project_name = input(
            "Por favor, ingresa el nombre de la aplicación principal del proyecto: ")
        
        creation = DjangoProjectManager(app_name=app_name, project_name=project_name)

        # Paso 2: Crear la aplicación "Home" si no existe
        creation.create_app()

        # Agregar automáticamente 'Home' a INSTALLED_APPS
        creation.installed_app()

        # Paso 3: Crear el archivo urls.py en la aplicación "Home" si no existe
        creation.create_urls(self.stdout)

        # Paso 4: Crear la carpeta services y el archivo authentication.py en Home
        creation.creation_auth(self.stdout)

        creation.create_views_urls(self. stdout)

        # Paso 8: Crear la carpeta templates y estatic y los archivos HTML CSS y JS
        templates_dir = os.path.join(app_name, 'templates')
        static_dir = os.path.join(app_name, 'static')

        # creacion de sub carpetas
        layouts_dir = os.path.join(templates_dir, 'layouts')
        js_dir = os.path.join(static_dir, 'js')
        css_dir = os.path.join(static_dir, 'css')

        # Crear las carpetas principales y subcarpetas
        os.makedirs(templates_dir, exist_ok=True)
        os.makedirs(static_dir, exist_ok=True)
        os.makedirs(layouts_dir, exist_ok=True)
        os.makedirs(js_dir, exist_ok=True)
        os.makedirs(css_dir, exist_ok=True)

        # creacion de los archivos

        js_file_path = os.path.join(js_dir, 'alertErrors.js')

        css_file_path = os.path.join(css_dir, 'authentication.css')

        layout_files_path = os.path.join(layouts_dir, 'index.html')

        template_files = {
            'home.html': """{% extends "layouts/index.html" %}
{% block layout %}
{% endblock %}""",
            'signup.html': """{% extends "layouts/index.html" %}
{% block layout %}
{% if error %}
<div class="alert" id="alert">
    <div class="alert-content">
        {{ error }}
        <button class="close-btn" onclick="closeAlert()">
            <span class="sr-only">Close</span>
            <svg class="close-icon" width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M0.92524 0.687069C1.126 0.486219 1.39823 0.373377 1.68209 0.373377C1.96597 0.373377 2.2382 0.486219 2.43894 0.687069L8.10514 6.35813L13.7714 0.687069C13.8701 0.584748 13.9882 0.503105 14.1188 0.446962C14.2494 0.39082 14.3899 0.361248 14.5321 0.360026C14.6742 0.358783 14.8151 0.38589 14.9468 0.439762C15.0782 0.493633 15.1977 0.573197 15.2983 0.673783C15.3987 0.774389 15.4784 0.894026 15.5321 1.02568C15.5859 1.15736 15.6131 1.29845 15.6118 1.44071C15.6105 1.58297 15.5809 1.72357 15.5248 1.85428C15.4688 1.98499 15.3872 2.10324 15.2851 2.20206L9.61883 7.87312L15.2851 13.5441C15.4801 13.7462 15.588 14.0168 15.5854 14.2977C15.5831 14.5787 15.4705 14.8474 15.272 15.046C15.0735 15.2449 14.805 15.3574 14.5244 15.3599C14.2437 15.3623 13.9733 15.2543 13.7714 15.0591L8.10514 9.38812L2.43894 15.0591C2.23704 15.2543 1.96663 15.3623 1.68594 15.3599C1.40526 15.3574 1.13677 15.2449 0.938279 15.046C0.739807 14.8474 0.627232 14.5787 0.624791 14.2977C0.62235 14.0168 0.730236 13.7462 0.92524 13.5441L6.59144 7.87312L0.92524 2.20206C0.724562 2.00115 0.611816 1.72867 0.611816 1.44457C0.611816 1.16047 0.724562 0.887983 0.92524 0.687069Z" fill="currentColor"/>
            </svg>
        </button>
    </div>
</div>
{% endif %}\n
<div class="form-wrapper">
    <div class="form-container">
        <form action="" method="post" class="form-control">
            {% csrf_token %}
            <h1>sing up</h1>

            <label for="username">Usuario:</label>
            {{ form.username }}

            <label for="password1">Contraseña:</label>
            {{ form.password1 }}

            <label for="password2">Confirmar Contraseña:</label>
            {{ form.password2 }}

            <button type="submit">sing Up</button>
        </form>
    </div>
</div>
{% endblock %}
""",
            'login.html': """{% extends "layouts/index.html" %}
{% block layout %}
{% if error %}
<div class="alert" id="alert">
    <div class="alert-content">
        {{ error }}
        <button class="close-btn" onclick="closeAlert()">
            <span class="sr-only">Close</span>
            <svg class="close-icon" width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M0.92524 0.687069C1.126 0.486219 1.39823 0.373377 1.68209 0.373377C1.96597 0.373377 2.2382 0.486219 2.43894 0.687069L8.10514 6.35813L13.7714 0.687069C13.8701 0.584748 13.9882 0.503105 14.1188 0.446962C14.2494 0.39082 14.3899 0.361248 14.5321 0.360026C14.6742 0.358783 14.8151 0.38589 14.9468 0.439762C15.0782 0.493633 15.1977 0.573197 15.2983 0.673783C15.3987 0.774389 15.4784 0.894026 15.5321 1.02568C15.5859 1.15736 15.6131 1.29845 15.6118 1.44071C15.6105 1.58297 15.5809 1.72357 15.5248 1.85428C15.4688 1.98499 15.3872 2.10324 15.2851 2.20206L9.61883 7.87312L15.2851 13.5441C15.4801 13.7462 15.588 14.0168 15.5854 14.2977C15.5831 14.5787 15.4705 14.8474 15.272 15.046C15.0735 15.2449 14.805 15.3574 14.5244 15.3599C14.2437 15.3623 13.9733 15.2543 13.7714 15.0591L8.10514 9.38812L2.43894 15.0591C2.23704 15.2543 1.96663 15.3623 1.68594 15.3599C1.40526 15.3574 1.13677 15.2449 0.938279 15.046C0.739807 14.8474 0.627232 14.5787 0.624791 14.2977C0.62235 14.0168 0.730236 13.7462 0.92524 13.5441L6.59144 7.87312L0.92524 2.20206C0.724562 2.00115 0.611816 1.72867 0.611816 1.44457C0.611816 1.16047 0.724562 0.887983 0.92524 0.687069Z" fill="currentColor"/>
            </svg>
        </button>
    </div>
</div>
{% endif %}
<div class="form-wrapper">\n
    <div class="form-container">
        <form action="" method="post" class="form-control">
            {% csrf_token %}
            <h1>Login</h1>

            <label for="username">Usuario:</label>
            {{ form.username }}

            <label for="password">Contraseña:</label>
            <input type="password" id="password" name="password" value="{{ form.password2 }}" required>

            <button type="submit">Login</button>
        </form>
    </div>
</div>
{% endblock %}
""",
            'logged.html': """{% extends "layouts/index.html" %}
{% block layout %}
  <div class="layout-container">
      <h1>¡Has iniciado sesión!</h1>
  </div>
{% endblock %}"""
        }
        for template_file, content in template_files.items():
            template_file_path = os.path.join(templates_dir, template_file)
            # escritura de los archivoos html
            write_file(template_file_path, content)

        # escritura de los archivos

        # escritura del archivos js
        write_file(js_file_path, """function closeAlert() {
    const alert = document.getElementById('alert');
        if (alert) {
            alert.remove();
        }
    }
    """)

        # escritura del archivo css
        write_file(css_file_path, """   
/* Navbar */
.navbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px 20px;
    background-color: #333; /* Color de fondo */
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

/* Logo */
.navbar .logo a {
    color: #ffffff;
    font-size: 1.5em;
    text-decoration: none;
    transition: color 0.3s ease;
}
                   
.navbar .logo a:hover {
    color: #4a90e2; /* Hover del logo */
}

/* Links de navegación */
.nav-links {
    display: flex;
    gap: 15px;
    list-style: none;
    margin: 0;
    padding: 0;
}

.nav-links .nav-item {
    color: #ffffff;
    font-size: 1em;
    text-decoration: none;
    padding: 8px 15px;
    border-radius: 5px;
    transition: background-color 0.3s ease, color 0.3s ease;
}

.nav-links .nav-item:hover {
    background-color: #4a90e2; /* Hover */
    color: #ffffff;
}

/* Estilos para dispositivos móviles */
.menu-toggle {
    display: none;
}

@media (max-width: 768px) {
    .menu-toggle {
        display: inline-block;
        font-size: 1.5em;
        color: #ffffff;
        cursor: pointer;
        padding: 8px 15px;
    }

    .nav-links {
        flex-direction: column;
        position: absolute;
        top: 100%;
        right: 0;
        width: 100%;
        background-color: #333;
        max-height: 0;
        overflow: hidden;
        transition: max-height 0.3s ease;
    }

    /* Activar menú desplegable */
    .nav-links.active {
        max-height: 300px; /* Ajustar altura */
    }

    .nav-links .nav-item {
        padding: 10px 20px;
    }
}

/*  formularios  */
/* Contenedor para centrar el formulario */
.form-wrapper {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-top: 50px;
}

/* Contenedor del formulario */
.form-container {
    padding: 20px;
    background: black; /* Fondo azul con transparencia */
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    color: white;
    text-align: center;
    max-width: 400px;
    width: 100%;
}

/* Estilo del formulario */
.form-control {
    display: flex;
    flex-direction: column;
    gap: 15px;
}

/* Estilo para las etiquetas */
label {
    font-size: 0.9em;
    color: #d1d5db; /* Color gris claro */
    margin-bottom: 5px;
    text-align: left;
}

/* Estilo para los campos de entrada */
input[type="text"],
input[type="password"] {
    padding: 10px;
    background: rgba(255, 255, 255, 0.2);
    border: 1px solid rgba(255, 255, 255, 0.3);
    border-radius: 5px;
    color: #ffffff;
    outline: none;
    font-size: 1em;
    transition: background 0.3s ease, box-shadow 0.3s ease;
}

input[type="text"]:focus,
input[type="password"]:focus {
    background: rgba(255, 255, 255, 0.4);
    box-shadow: 0 0 5px rgba(255, 255, 255, 0.5);
}

/* Estilo del botón */
button[type="submit"] {
    padding: 10px;
    background: #4a90e2;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    transition: background 0.3s ease;
}

button[type="submit"]:hover {
    background: #357ab8;
}
            
/* alert */

/* Estilos para la alerta */
.alert {
    max-width: 400px;
    background-color: #333;
    color: #ffffff;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    margin: 0 auto;
    position: relative;
    top: 20px;
    padding: 15px;
}

.alert-content {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.close-btn {
    background: none;
    border: none;
    cursor: pointer;
    color: #ffffff;
    transition: color 0.3s ease;
}

.close-btn:hover {
    color: #ff6b6b;
}

.close-icon {
    width: 16px;
    height: 16px;
}

/* logged */

/* Estilos para el contenedor del bloque */
.layout-container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    background-color: #f0f4f8;
    font-family: Arial, sans-serif;
}                   

/* Estilos para el título */
.layout-container h1 {
    font-size: 2.5rem;
    color: #4a90e2;
    font-weight: bold;
    text-align: center;
    padding: 20px;
    border-radius: 8px;
    background: #ffffff;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}
""")
        # escritura del archivos que estan en la carpeta layouts
        write_file(layout_files_path, """{% load static %}
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="{% static 'css/authentication.css' %}">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.6.0/css/all.min.css">
    <title>django components</title>
</head>
<body class="bg-gray-100 text-gray-800">
                    
<nav class="navbar">
    <div class="logo">
        <a href="{% url 'home' %}">
            <i class="fa-solid fa-house"></i>
        </a>
    </div>
    <div class="menu-toggle">
        <i class="fa fa-bars"></i>
    </div>
    <ul class="nav-links">
        {% if user.is_authenticated %}
            <li><a href="{% url 'logout' %}" class="nav-item">Logout</a></li>
        {% else %}
            <li><a href="{% url 'signup' %}" class="nav-item">Sign Up</a></li>
            <li><a href="{% url 'login' %}" class="nav-item">Login</a></li>
        {% endif %}
    </ul>
</nav>

<div class="container mx-auto p-4">
    {% block layout %}
    {% endblock %}
</div>

<script src="{% static 'js/alertErrors.js'%}"></script>
</body>
</html>
""")

        self.stdout.write(self.style.SUCCESS(
            "Comando ejecutado exitosamente."))
