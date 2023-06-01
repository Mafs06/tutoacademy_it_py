# Utiliza la imagen base de Python
FROM python:3.9

# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia los archivos necesarios al contenedor
COPY . .

# Instala las dependencias
RUN pip install --no-cache-dir spyne requests

# Expone el puerto 8100
EXPOSE 8100

# Ejecuta el comando para iniciar la aplicación
CMD [ "python", "./soapExpose.py" ]
