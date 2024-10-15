from django.conf import settings
import redis

class ContadorVisitasMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.redis_conn = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)

    def __call__(self, request):
        # Incrementa el contador para cualquier solicitud
        self.redis_conn.incr('visitas_totales')
        # Incrementa el contador por sesión de usuario
        if request.session.session_key:
            if 'visita_registrada' not in request.session:
                self.redis_conn.incr('visitas_sesion')
                print('visitas_registrada')
                # Marca la visita como registrada para esta sesión
                request.session['visita_registrada'] = True

        return self.get_response(request)

