import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "recetas_lukas.settings")
django.setup()

from django.core.management.base import BaseCommand
from core.models import ItemsPagina
from django.utils.text import slugify

class Command(BaseCommand):
    help = 'Genera slugs para registros existentes sin slug'

    def handle(self, *args, **options):
        items = ItemsPagina.objects.filter(slug__isnull=True)
        for item in items:
            item.slug = slugify(item.titulo)  # Reemplaza 'titulo' con el campo que deseas usar para generar el slug
            item.save()
        self.stdout.write(self.style.SUCCESS('Se han generado slugs para registros existentes sin slug'))
