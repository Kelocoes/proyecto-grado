[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=Kelocoes_proyecto-grado&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=Kelocoes_proyecto-grado)
[![Duplicated Lines (%)](https://sonarcloud.io/api/project_badges/measure?project=Kelocoes_proyecto-grado&metric=duplicated_lines_density)](https://sonarcloud.io/summary/new_code?id=Kelocoes_proyecto-grado)
[![Vulnerabilities](https://sonarcloud.io/api/project_badges/measure?project=Kelocoes_proyecto-grado&metric=vulnerabilities)](https://sonarcloud.io/summary/new_code?id=Kelocoes_proyecto-grado)
[![Bugs](https://sonarcloud.io/api/project_badges/measure?project=Kelocoes_proyecto-grado&metric=bugs)](https://sonarcloud.io/summary/new_code?id=Kelocoes_proyecto-grado)
[![Code Smells](https://sonarcloud.io/api/project_badges/measure?project=Kelocoes_proyecto-grado&metric=code_smells)](https://sonarcloud.io/summary/new_code?id=Kelocoes_proyecto-grado)
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

Se aclara que es requerido un archivo `.env` con la siguiente estructura: \
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

Esto es necesario para las siguientes acciones:
- Credenciales de la base de datos
- Llaves para la encripcación AES 256, Modo CBC
- Credenciales para envío de correos
- Llave para uso de la api de reCaptcha
- URL del Front-End

# Nota del creador
Este proyecto incluyendo el componente front se hizo con mucho empeño durante el año 2023.
- [Repositorio del Front-End](https://github.com/Kelocoes/proyecto-grado-front)
