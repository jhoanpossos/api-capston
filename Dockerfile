# Usar una imagen base oficial de Python
FROM python:3.10-slim

# Instalar dependencias del sistema operativo, incluyendo los drivers de ODBC
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    gnupg \
    unixodbc-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Añadir el repositorio de Microsoft para los drivers de SQL Server
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list

# Instalar el driver de SQL Server
RUN apt-get update && ACCEPT_EULA=Y apt-get install -y msodbcsql18

# Crear un directorio para la aplicación dentro del contenedor
WORKDIR /app

# Copiar el archivo de requerimientos e instalar las librerías de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código de la aplicación
COPY . .

# Exponer el puerto que Gunicorn usará
EXPOSE 8000

# Comando final para iniciar la aplicación (el mismo que tenías)
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--timeout", "600", "app:app"]