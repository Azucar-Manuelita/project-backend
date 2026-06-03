from django.http import JsonResponse
from .models import Goal


def prueba_conexion(request):
    # Creamos un dato de prueba en la BD
    meta, created = Goal.objects.get_or_create(
        name="Ganar masa muscular",
        defaults={'description': 'Aumentar volumen mediante hipertrofia'}
    )
   
    return JsonResponse({
        "status": "¡Conexión Exitosa!",
        "database": "PostgreSQL",
        "dato_recuperado": {
            "id": meta.id,
            "meta": meta.name
        }
    })
