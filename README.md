Este projecto esta escrito en python con Django, es la prueba tecnica para la posición Backend de Zebrands.

En el archivo de vies se encuentra toda la logica para hacer el crud, se usaron sesiones para el ingreso 
de administradores que pudieran dar de alta productos y nuevos administradores, además de que se valido para que los que no tuvieran permisos de editar no pudieran ver las opciones de un "super administrador"

La funcionalidad el codigo se encuentra documento en cada linea dentro del views

Usuarios:
SuperAdmin 
Admin
abc

Contraseñas:
root
090807
abc

Donde pueden editar:
SuperAdmin y abc


Notificaciones:
Se usaron notificaciones en un canal de Telegram el link para poder unirse a dicho canal y ver las notificaciones de cuando un producto se modifica es: https://t.me/notificationsproducts


Instrucciones:
Ubicarse en la carpeta "backend-test-zebrands/zebrand" y ejecutar el comando python manage.py runserver para iniciar el proyecto.

Este se podra visualizar desde el navegador en la ruta http://127.0.0.1:8000

