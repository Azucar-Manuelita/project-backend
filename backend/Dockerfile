# 1. Definir la imagen base de Python
FROM python:3.12-slim

# 2. Establecer el directorio de trabajo dentro del contenedor
WORKDIR /code

# 3. Copiar el archivo de dependencias primero para optimizar caché
COPY requirements.txt .

# 4. Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copiar el resto del código fuente al contenedor
COPY . .

# 6. Definir el comando para ejecutar la aplicación
CMD ["python", "gym_app.py"]
