from django.core.management.base import BaseCommand, CommandError
from django.apps import apps
import os

class Command(BaseCommand):
    help = 'Crear un archivo HTML dentro de la carpeta templates o static de una app'

    def add_arguments(self, parser):
        parser.add_argument('app_name', type=str, help='Nombre de la app')
        parser.add_argument('file_path', type=str, help='Ruta del componente HTML')
        parser.add_argument(
            '--type', 
            type=str, 
            choices=['template', 'static'], 
            default='template', 
            help='Tipo de archivo a crear: "template" para archivos en la carpeta templates, "static" para archivos en la carpeta static'
        )

    def handle(self, *args, **kwargs):
        app_name = kwargs['app_name']
        file_path = kwargs['file_path']
        file_type = kwargs['type']

        try:
            app_config = apps.get_app_config(app_name)
        except LookupError:
            raise CommandError(f'App "{app_name}" no encontrada.')

        base_dir = os.path.join(app_config.path, 'templates' if file_type == 'template' else 'static')

        if not os.path.exists(base_dir):
            os.makedirs(base_dir)

        file_full_path = os.path.join(base_dir, file_path)
        file_full_path = os.path.normpath(file_full_path)

        file_folder = os.path.dirname(file_full_path)
        if not os.path.exists(file_folder):
            os.makedirs(file_folder)

        if os.path.exists(file_full_path):
            self.stdout.write(self.style.WARNING(f'El archivo {file_path} ya existe en {app_name}/{file_type}/.'))
        else:
            file_extension = os.path.splitext(file_path)[1]
            if file_extension == '.html':
                content = '<div>Este es el contenido del componente.</div>'
            elif file_extension == '.js':
                content = 'console.log("Este es el contenido del componente.");'
            elif file_extension == '.css':
                content = '/* Este es el contenido del componente */'
            else:
                content = ''

            with open(file_full_path, 'w') as f:
                f.write(content)

            self.stdout.write(self.style.SUCCESS(f'Se creó correctamente {file_path} en {app_name}/{file_type}/.'))
