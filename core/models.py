import os

from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import User
from easy_thumbnails.fields import ThumbnailerImageField
from easy_thumbnails.files import get_thumbnailer
from taggit.managers import TaggableManager
from easy_thumbnails.exceptions import InvalidImageFormatError
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files.base import ContentFile
from django.contrib.postgres.indexes import GinIndex
from django.utils.text import slugify
from autoslug import AutoSlugField

# Create your models here.
class ItemsPagina(models.Model):
    class Status(models.TextChoices):
        CREADO = 'CR', 'Creado'
        PUBLICADO = 'PB', 'Publicado'
    CATEGORIAS = [
        ('car', 'Carne'),
        ('pes', 'Pescado'),
        ('ave', 'Ave'),
        ('cal', 'Caldo'),
        ('ens', 'Ensalada'),
        ('pas', 'Pasta'),
        ('pos', 'Postre'),
        ('sop', 'Sopa'),
        ('ver', 'Verdura'),
        ('otr', 'Otro'),]

    titulo = models.CharField(max_length=250)
    contenido = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.CREADO)
    imagen = ThumbnailerImageField(upload_to='pasos_pics', blank=True, null=True)
    likes = models.ManyToManyField(User, related_name='likes', blank=True)
    tags = TaggableManager(blank=True)
    categoria = models.CharField(max_length=25, choices=CATEGORIAS, default="ning")
    slug = AutoSlugField(unique=True, populate_from='titulo')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titulo)

        if self.imagen:
            try:
                img = Image.open(self.imagen)
                img = img.resize((800, 600))
                # Convertir la imagen a formato JPEG
                buffer = BytesIO()
                img.save(buffer, format='JPEG')
                buffer.seek(0)
                # Sobrescribir la imagen original con la nueva imagen
                self.imagen = InMemoryUploadedFile(buffer, None, 'imagen.jpg', 'image/jpeg', buffer.getbuffer().nbytes, None)
            except Exception as e:
                print(f"Error al procesar la imagen: {e}")
        super().save(*args, **kwargs)

    @property
    def tiempo_total(self):
        return self.pasos_set.aggregate(Sum('tiempo_preparacion'))['tiempo_preparacion__sum'] or 0

    def __str__(self):
        return self.titulo

    class Meta:
        ordering = ['fecha_creacion', 'fecha_modificacion']
        indexes = [
            models.Index(fields=['titulo'], name='titulo_index', opclasses=['varchar_pattern_ops']),
            models.Index(fields=['-fecha_creacion', 'categoria']),
            GinIndex(fields=['titulo'], name='titulo_gin_index', opclasses=['gin_trgm_ops']),
        ]


class Pasos(models.Model):
    numero = models.IntegerField()
    descripcion = models.CharField(max_length=250)
    imagen_paso = ThumbnailerImageField(upload_to='recetas_pics', blank=True, null=True)
    recetas = models.ForeignKey(ItemsPagina, on_delete=models.CASCADE)
    tiempo_preparacion = models.IntegerField()
    tiempo_coccion = models.IntegerField()

    def save(self, *args, **kwargs):
        if self.imagen_paso:
            try:
                thumbnail = self.imagen_paso.get_thumbnail({'size': (800, 600), 'crop': True})
                thumbnail_content = thumbnail.read()
                # Generar un nombre único para la miniatura
                thumbnail_name = f"thumbnail_{os.path.basename(self.imagen_paso.name)}"
                # Guardar la miniatura en un ContentFile
                thumbnail_path = self.imagen_paso.storage.save(thumbnail_name, ContentFile(thumbnail_content))
                # Actualizar el campo de imagen_paso con la ruta de la miniatura
                self.imagen_paso = thumbnail_path
            except InvalidImageFormatError:
                pass
        super().save(*args, **kwargs)

    class Meta:
        indexes = [
            GinIndex(fields=['descripcion'], name='descripcion_gin_index', opclasses=['gin_trgm_ops']),
        ]


class Ingredientes(models.Model):
    nombre = models.CharField(max_length=250)
    cantidad = models.CharField(max_length=250)
    recetas = models.ForeignKey(ItemsPagina, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

    class Meta:
        indexes = [
            GinIndex(fields=['nombre'], name='nombre_gin_index', opclasses=['gin_trgm_ops']),
        ]
