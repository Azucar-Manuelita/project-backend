@echo off
setlocal enabledelayedexpansion

:: Cambia al directorio del script
pushd "%~dp0"

:: Construye e inicia los contenedores de Docker
echo Construyendo e iniciando los contenedores...
docker-compose up -d --build

:: Espera a que el contenedor web responda correctamente
echo Esperando a que el contenedor web este listo...
set count=0
:wait_loop
set /a count+=1
docker-compose exec web python manage.py check >nul 2>&1
if %errorlevel%==0 goto web_ready
echo Esperando 3 segundos... (%count%/20)
timeout /t 3 /nobreak >nul
if %count% GEQ 20 goto web_failed
goto wait_loop

:web_ready
echo Contenedor web listo.

:: Crear gym_app solo si no existe
if not exist "backend\gym_app" (
    echo Creando la aplicacion gym_app...
    docker-compose exec web python manage.py startapp gym_app
) else (
    echo La aplicacion gym_app ya existe. Se omite startapp.
)

:: Generar migraciones para gym_app
echo Generando migraciones para gym_app...
docker-compose exec web python manage.py makemigrations gym_app

:: Aplicar migraciones a la base de datos
echo Aplicando migraciones...
docker-compose exec web python manage.py migrate

:done
echo Configuracion inicial completada. El servidor Django esta disponible en http://localhost:8000
popd
goto eof

:web_failed
echo Error: el contenedor web no respondio correctamente despues de 20 intentos.
popd
exit /b 1
