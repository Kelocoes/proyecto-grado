# Backend - Proyecto de Grado
Estimación de riesgo cardiovascular en Colombia utilizando técnicas de inteligencia artificial.
- Creado por Kevin David Rodríguez Belalcázar

# Ejecución
Para instalar las dependencias de este proyecto puedes usar el archivo *build.sh*.
- Python: 3.11.3
- Pip: 22.3.1

Puede ejecutarse de forma local por medio del comando *python manage.py runserver*.\
Se aclara que es requerido un archivo *.env* con la siguiente estructura: \
&nbsp;&nbsp; DB_NAME=...\
&nbsp;&nbsp; DB_USER=...\
&nbsp;&nbsp; DB_PASSWORD=...\
&nbsp;&nbsp; DB_HOST=...\
&nbsp;&nbsp; DB_DATABASE_PORT=...\
&nbsp;&nbsp; AES_IV=...\
&nbsp;&nbsp; AES_SECRET_KEY=...\
&nbsp;&nbsp; SENDER_ADDRESS=...\
&nbsp;&nbsp; SENDER_PASS=...\
&nbsp;&nbsp; CAPTCHA_SECRET_KEY=...\
&nbsp;&nbsp; FRONT_URL=...

Esto para las credenciales de la base de datos a utilizar y las llaves de la encriptación usando AES 256 en modo CBC (Hay mejores pero no quiero gastar tanto tiempo en ello).\
También para envío de correos.\
Y también para el captcha.\
Y también para el envío de correos.

### Nota del creador
Este proyecto incluído el componente front se hizo con mucho empeño durante el año 2023.
