# Utiliza una imagen base de Python
FROM python:3.9-slim

# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia todos los archivos del proyecto al contenedor
COPY . /app

# Instala las dependencias de Python desde requirements.txt
RUN pip install -r requirements.txt

# Crea las bases de datos y tablas desde el script db.sql
# Asume que tienes acceso a MySQL o PostgreSQL
# Asegúrate de tener configuradas las variables de entorno necesarias para MySQL en tu archivo .env

# Aquí suponemos que ya tienes un archivo .env que contiene las credenciales
# De ser necesario, agrega este comando para cargarlas:
RUN python -c "from dotenv import load_dotenv; load_dotenv()"

# Comando para crear las bases de datos y las tablas (carga el script db.sql)
RUN mysql -u $MYSQL_USER -p$MYSQL_PASSWORD -h $MYSQL_HOST -e "source db.sql"

# Poblar las bases de datos usando el script populate_db.py
RUN python populate_db.py

# Exponer el puerto para el servidor web (generalmente 5000 para Flask, o el que uses en tu app)
EXPOSE 5000

# Ejecutar la aplicación Flask con app.py
CMD ["python", "app.py"]
