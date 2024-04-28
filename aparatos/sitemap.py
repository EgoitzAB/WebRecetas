from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from .models import Aparatos, Modelos


class AparatosSitemap(Sitemap):
    def items(self):
        return ['aparatos:aparatos_lista', 'aparatos:aparatos_detalle']

    def location(self, item):
        return reverse(item)

    def priority(self, item):
        return 1.0

    def changefreq(self, item):
        return 'monthly'

#    def lastmod(self, item):
#        if item == 'aparatos:aparatos_lista':
#            return Aparatos.objects.latest('modelo__fecha_modificacion').modelo.fecha_modificacion
#        elif item == 'aparatos:aparatos_detalle':
#            return Aparatos.objects.latest('modelo__fecha_modificacion').modelo.fecha_modificacion

    def lastmod(self, item):
        if item == 'aparatos:aparatos_lista' or item == 'aparatos:aparatos_detalle':
            try:
                latest_modelo = Modelos.objects.latest('fecha_modificacion')
                return latest_modelo.fecha_modificacion
            except ObjectDoesNotExist:
                # Manejar el caso en el que no hay modelos disponibles
                # Puedes devolver la fecha actual o None según sea necesario
                return None
