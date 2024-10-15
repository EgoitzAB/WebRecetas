from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import ItemsPagina


class RecetasSitemap(Sitemap):
    def items(self):
        return ['core:home', 'core:receta_lista', 'core:recetas']

    def location(self, item):
        return reverse(item)

    def priority(self, item):
        return 1.0

    def changefreq(self, item):
        return 'monthly'

    def lastmod(self, item):
        if item == 'core:home':
            return ItemsPagina.objects.latest('updated').updated
        elif item == 'core:recetas':
            return ItemsPagina.objects.latest('updated').updated
        elif item == 'core:receta_lista':
            return ItemsPagina.objects.latest('updated').updated