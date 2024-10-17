# Usa una imagen base de Python
FROM python:3.11-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia el archivo de requisitos
COPY requirements.txt /app/

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto de la aplicación
COPY . /app/

# Expone el puerto 8000 para Django
EXPOSE 8000

# Comando para ejecutar el servidor de Django
CMD ["python", "manage.py", "runsslserver", "0.0.0.0:8000"]
