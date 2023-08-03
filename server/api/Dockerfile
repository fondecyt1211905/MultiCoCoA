FROM python:3.9.12

# Establecer el directorio de trabajo
WORKDIR /app

RUN apt-get update && apt-get install -y libgl1-mesa-glx

# Copiar los archivos necesarios al contenedor
COPY ./ ./

# Instalar las dependencias
RUN pip install -r requirements.txt

# Exponer el puerto que utiliza la aplicación
EXPOSE 80

# Definir el comando para ejecutar la aplicación
CMD ["sh", "-c", "python app.py & python streamAudio.py & python streamVideo.py"]