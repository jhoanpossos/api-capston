#!/bin/bash

# Instalar las dependencias de ODBC para pyodbc
apt-get update
apt-get install -y unixodbc-dev

# Instalar el driver oficial de Microsoft
curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
curl https://packages.microsoft.com/config/ubuntu/20.04/prod.list > /etc/apt/sources.list.d/mssql-release.list
apt-get update
ACCEPT_EULA=Y apt-get install -y msodbcsql18

# Iniciar la aplicación con Gunicorn (el comando que ya tenías)
gunicorn --bind=0.0.0.0 --timeout 600 app:app
