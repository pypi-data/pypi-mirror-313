# componentsDjangotype

<div style="center">
  <img src="https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white" alt="Django">
  <img src="https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54" alt="Python">
  <img src="https://img.shields.io/badge/pypi-%23ececec.svg?style=for-the-badge&logo=pypi&logoColor=1f73b7" alt="PyPi">
</div>

# Comando de Creación de Componentes HTML de Django

Este comando de Django te permite crear un componente HTML dentro del directorio `templates` o `static` de una aplicación específica.

## Instalación

1. Instala Django si no lo has hecho ya: `pip install django`
2. Luego instala el paquete pip `pip install componentsDjangoType`
3. Agrega `componentsDjangoType` a la lista de aplicaciones instaladas (`INSTALLED_APPS`) en el archivo `settings.py` de tu proyecto de Django.

## Uso

### comando para hacer archivos html css y js

1. Ejecuta el comando en tu terminal: `python manage.py myapp createcomponent <carpeta/archivo> --type=<template|static>`
2. Reemplaza `<nombre_de_aplicación>`con el nombre de la aplicación donde deseas crear el componente.
3. Reemplaza `<ruta_del_archivo>` con la ruta donde deseas crear el componente dentro del directorio templates o static de la aplicación.
4. La bandera `--type` especifica si deseas crear un componente en el directorio templates o static. Por defecto, se establece en template.

### comando para crear una app para autenticación

1. Ejecuta el comando en tu terminal: `python manage.py createApp`
2. En este punto te mostrara un mensaje para poner el nombre de la app principal de tu apicacion
la App principal es la que tiene el archivo settings.py de tu aplicacion

## Ejemplo

Para crear un componente HTML en el directorio `templates` de la aplicación `myapp` con la ruta `components/my_component.html`, ejecuta:
```
python manage.py myapp components/my_component.html --type static
```

## Notas

- El comando creará los directorios necesarios si no existen.
- Si el archivo del componente ya existe, el comando mostrará un mensaje de advertencia.
- El comando creará un contenido predeterminado para el componente según su extensión de archivo:
    - `.html`: `<div>Este es el contenido del componente.</div>`
    - `.js`: `console.log("Este es el contenido del componente.");`
    - `.css`: `/* Este es el contenido del componente */`
- Si buscas el paquete de pip para descargarlo, aquí está: [Pypi](https://pypi.org/project/componentsDjangoType/)

## Licencia

Este proyecto está licenciado bajo la Licencia MIT. Consulta el archivo [LICENSE](LICENSE) para obtener más detalles.
