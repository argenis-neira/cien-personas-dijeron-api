# Usa la imagen oficial de Python desde Docker Hub
FROM python:3.9-slim

# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia los archivos necesarios al contenedor
COPY . .

# Instala las dependencias especificadas en requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expone el puerto 8080 para que pueda ser accesible
EXPOSE 8080

# Define el comando por defecto para ejecutar tu aplicación en el contenedor
CMD ["python", "app.py"]
