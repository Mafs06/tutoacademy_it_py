# Utiliza la imagen base de Python
FROM python:3

# Establece el directorio de trabajo en /app
WORKDIR /app

# Instala las dependencias

RUN pip install spyne 
RUN pip install requests 
RUN pip install lxml

# Copia los archivos necesarios al contenedor
COPY ./ ./

# Expone el puerto 8100
EXPOSE 8100

# Ejecuta el comando para iniciar la aplicación
CMD [ "python", "soapExpose.py" ]
