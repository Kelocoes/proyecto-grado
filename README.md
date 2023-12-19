[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=Kelocoes_proyecto-grado&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=Kelocoes_proyecto-grado)
[![Duplicated Lines (%)](https://sonarcloud.io/api/project_badges/measure?project=Kelocoes_proyecto-grado&metric=duplicated_lines_density)](https://sonarcloud.io/summary/new_code?id=Kelocoes_proyecto-grado)
[![Vulnerabilities](https://sonarcloud.io/api/project_badges/measure?project=Kelocoes_proyecto-grado&metric=vulnerabilities)](https://sonarcloud.io/summary/new_code?id=Kelocoes_proyecto-grado)
[![Bugs](https://sonarcloud.io/api/project_badges/measure?project=Kelocoes_proyecto-grado&metric=bugs)](https://sonarcloud.io/summary/new_code?id=Kelocoes_proyecto-grado)
[![Code Smells](https://sonarcloud.io/api/project_badges/measure?project=Kelocoes_proyecto-grado&metric=code_smells)](https://sonarcloud.io/summary/new_code?id=Kelocoes_proyecto-grado)
[![Lines of Code](https://sonarcloud.io/api/project_badges/measure?project=Kelocoes_proyecto-grado&metric=ncloc)](https://sonarcloud.io/summary/new_code?id=Kelocoes_proyecto-grado)
# Backend - Proyecto de Grado
Estimación de riesgo cardiovascular en Colombia utilizando técnicas de inteligencia artificial.
- Creado por Kevin David Rodríguez Belalcázar
- Proyecto final de la carrera Ingeniería de Sistemas
- Universidad del Valle, Cali - Valle del Cauca, Colombia

# Ejecución
Para instalar las dependencias de este proyecto puedes usar el archivo `build.sh`.
- Python: 3.11.3
- Pip: 22.3.1

Puede ejecutarse de forma local por medio del comando:
```bash
    python manage.py runserver
```

Se aclara que es requerido un archivo `.env` con una estructura similar a la siguiente: \
&nbsp;&nbsp; DB_NAME=postgres \
&nbsp;&nbsp; DB_USER=user \
&nbsp;&nbsp; DB_PASSWORD=password \
&nbsp;&nbsp; DB_HOST=host \
&nbsp;&nbsp; DB_DATABASE_PORT=5432 \
&nbsp;&nbsp; AES_IV=YfQEdyEYuUBmunEU \
&nbsp;&nbsp; AES_SECRET_KEY=nEnWbpugBYUuIajgRStZbAWhrgyekggr \
&nbsp;&nbsp; SENDER_ADDRESS=mail@mail.com \
&nbsp;&nbsp; SENDER_PASS=password \
&nbsp;&nbsp; CAPTCHA_SECRET_KEY=6LeFACwnAAAAACj2jdTD9_rKx8rf4tz-Xxy1Xx0n \
&nbsp;&nbsp; FRONT_URL=http://localhost:3000

Esto es necesario para las siguientes acciones:
- Credenciales de la base de datos
- Llaves para la encriptación AES 256, Modo CBC (con longitud de 16 y 32 respectivamente)
- Credenciales para envío de correos (correo y contraseña)
- Llave para uso de la api de reCaptcha (revisar documentación de [google](https://www.google.com/recaptcha/about/))
- URL del Front-End (puede ser localhost en el puerto 3000 o la url donde está alojado el frontend)

# Nota del creador
Este proyecto incluyendo el componente front se hizo con mucho empeño durante el año 2023.
- [Repositorio del Front-End](https://github.com/Kelocoes/proyecto-grado-front)
