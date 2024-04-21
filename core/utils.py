import redis
from django.conf import settings
from .models import ItemsPagina

def obtener_vistas_de_receta(receta_id):
    # Conexión a Redis
    redis_connection = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)

    # Obtener el número de vistas de la receta
    key = f"receta:{receta_id}:vistas"
    vistas = redis_connection.get(key)

    print(f"Vistas de la receta {receta_id}: {vistas}")  # Imprimir el número de vistas de la receta

    return int(vistas) if vistas is not None else 0

def recetas_mas_vistas(request, cantidad_recetas=6):
    # Conexión a Redis
    redis_connection = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)

    # Obtener las IDs de las recetas más vistas
    ids_recetas = redis_connection.zrevrangebyscore('recetas_vistas', '+inf', '-inf', start=0, num=cantidad_recetas)

    print("IDs de recetas más vistas:", ids_recetas)  # Imprimir las IDs de las recetas más vistas

    # Obtener la información de las recetas más vistas
    recetas_mas_vistas = []
    for id_receta in ids_recetas:
        receta = ItemsPagina.objects.get(id=id_receta)
        recetas_mas_vistas.append(receta)

    print("Recetas más vistas:", recetas_mas_vistas)  # Imprimir la lista de recetas más vistas

    # Devolver las recetas más vistas
    return recetas_mas_vistas

