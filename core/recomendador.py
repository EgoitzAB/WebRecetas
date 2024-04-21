import redis
from django.conf import settings
from django.utils import timezone
from datetime import datetime, timedelta

# Conexión a Redis
r = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)

class RecetaRecomendador:
    def get_receta_key(self, receta_id):
        return f'receta:{receta_id}:vistas_junto_con'

    def recetas_vistas_junto_con(self, historial):
        recetas_ids = historial.get_recetas_ids()
        for receta_id in recetas_ids:
            for otra_id in recetas_ids:
                if receta_id != otra_id:
                    # Incrementar puntaje por receta vista junto con otra receta
                    r.zincrby(self.get_receta_key(receta_id), 1, otra_id)

    def sugerir_recetas_para(self, historial, max_resultados=6):
        recetas_ids = historial.get_recetas_ids()
        if len(recetas_ids) == 1:
            # Solo 1 receta en el historial
            sugerencias = r.zrange(
                self.get_receta_key(recetas_ids[0]), 0, -1, desc=True)[:max_resultados]
        else:
            # Combinar los puntajes de todas las recetas y almacenarlos en una clave temporal
            flat_ids = ''.join([str(id) for id in recetas_ids])
            tmp_key = f'tmp_{flat_ids}'
            keys = [self.get_receta_key(id) for id in recetas_ids]
            r.zunionstore(tmp_key, keys)
            r.zrem(tmp_key, *recetas_ids)
            sugerencias = r.zrange(tmp_key, 0, -1, desc=True)[:max_resultados]
            r.delete(tmp_key)
        sugerencias_ids = [int(id) for id in sugerencias]
        return sugerencias_ids


class RecetaHistorial:
    def __init__(self, request):
        """ Inicializar el historial de recetas vistas"""
        self.session = request.session
        self.session_start = self.session.get('_session_creation_time')  # Hora de inicio de la sesión
        if self.session_start is None:
            # Si la hora de inicio de la sesión no está definida, asignar la hora actual
            self.session_start = timezone.now().isoformat()
            self.session['_session_creation_time'] = self.session_start
        historial = self.session.get(settings.HISTORIAL_RECETAS_ID)
        if not historial:
            # guardar un historial vacío
            historial = self.session[settings.HISTORIAL_RECETAS_ID] = {}
        self.historial = historial

    def __len__(self):
        """
        Contar todos los items en el historial.
        """
        return sum(item['quantity'] for item in self.historial.values())

    def añadir(self, receta, quantity=1, override_quantity=False):
        """
        Añadir un producto al historial.
        """
        # Convertir la hora de inicio de la sesión a un objeto datetime
        session_start_datetime = datetime.fromisoformat(self.session_start)
        print(session_start_datetime)
        print(session_start_datetime + timedelta(hours=1) <= timezone.now())
        print(self.historial)
        if (session_start_datetime + timedelta(hours=1) <= timezone.now()) or (len(self.historial) >= 10):
        # Llamar a recetas_vistas_junto_con y limpiar el historial
            recomendador = RecetaRecomendador()
            recomendador.recetas_vistas_junto_con(self)
            print("Recetas vistas juntas actualizadas.")
            self.session[settings.HISTORIAL_RECETAS_ID] = {}
            print("Recomendaciones limpiadas.")

            # Actualizar la hora de inicio de la sesión para la próxima vez
            self.session_start = timezone.now().isoformat()
            self.session['_session_creation_time'] = self.session_start
        receta_id = str(receta.id)
        if receta_id not in self.historial:
            self.historial[receta_id] = 1
        self.save()
        print("Receta añadida al historial.")

    def save(self):
        # marcar la session como modificada para estar seguro de su guardado
        self.session.modified = True

    def get_recetas_ids(self):
        """Obtener los IDs de todas las recetas en el historial."""
        return [int(receta_id) for receta_id in self.historial.keys()]
