#!/bin/bash

set -e

# Cambia al directorio donde está este script.
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

# Levanta los servicios de Docker y reconstruye la imagen si es necesario.
echo "Construyendo e iniciando los contenedores..."
docker-compose up -d --build

# Espera a que Django responda correctamente dentro del contenedor web.
echo "Esperando a que el contenedor web esté listo..."
count=0
until docker-compose exec web python manage.py check >/dev/null 2>&1; do
  count=$((count + 1))
  if [ "$count" -ge 20 ]; then
    echo "Error: el contenedor web no respondió correctamente después de 20 intentos."
    exit 1
  fi
  echo "Esperando 3 segundos... ($count/20)"
  sleep 3
done

echo "Contenedor web listo."

# Crea gym_app solo si aún no existe en el directorio backend.
if [ ! -d backend/gym_app ]; then
  echo "Creando la aplicación gym_app..."
  docker-compose exec web python manage.py startapp gym_app
else
  echo "La aplicación gym_app ya existe. Se omite startapp."
fi

# Prepara las migraciones específicas de gym_app.
echo "Generando migraciones para gym_app..."
docker-compose exec web python manage.py makemigrations gym_app

# Aplica las migraciones a la base de datos PostgreSQL.
echo "Aplicando migraciones..."
docker-compose exec web python manage.py migrate

echo "Configuración inicial completada. El servidor Django está disponible en http://localhost:8000"

