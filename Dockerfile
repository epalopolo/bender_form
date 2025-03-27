# Usamos una imagen base de Python
FROM python:3.8-slim

# Establecemos el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiamos el archivo requirements.txt al contenedor
COPY requirements.txt .

# Instalamos dependencias del sistema necesarias (como gcc, libmysqlclient-dev)
RUN apt-get update && apt-get install -y \
    gcc \
    libmysqlclient-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Instalamos las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el resto del código de la aplicación
COPY . .

# Exponemos el puerto en el que la app va a correr
EXPOSE 8000

# Comando para ejecutar la app
CMD ["python", "app.py"]

