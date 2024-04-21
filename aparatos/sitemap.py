from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Aparatos


class AparatosSitemap(Sitemap):
    def items(self):
        return ['aparatos:aparatos_lista', 'aparatos:aparatos_detalle']

    def location(self, item):
        return reverse(item)

    def priority(self, item):
        return 1.0

    def changefreq(self, item):
        return 'monthly'

    def lastmod(self, item):
        if item == 'aparatos:aparatos_lista':
            return Aparatos.objects.latest('modelos').fecha_modificacion
        elif item == 'aparatos:aparatos_detalle':
            return Aparatos.objects.latest('modelos').fecha_modificacion