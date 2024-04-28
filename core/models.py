import os
import uuid

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
        ('carne', 'Carne'),
        ('pescado', 'Pescado'),
        ('ave', 'Ave'),
        ('caldo', 'Caldo'),
        ('ensalada', 'Ensalada'),
        ('pasta', 'Pasta'),
        ('postre', 'Postre'),
        ('sopa', 'Sopa'),
        ('verdura', 'Verdura'),
        ('otro', 'Otro'),]

    titulo = models.CharField(max_length=250)
    autor = models.CharField(max_length=100, default="Lucas")
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
        tiempo_preparacion_total = self.pasos_set.aggregate(Sum('tiempo_preparacion'))['tiempo_preparacion__sum'] or 0
        tiempo_coccion_total = self.pasos_set.aggregate(Sum('tiempo_coccion'))['tiempo_coccion__sum'] or 0
        tiempo_total_combinado = tiempo_preparacion_total + tiempo_coccion_total
        return tiempo_preparacion_total, tiempo_coccion_total, tiempo_total_combinado

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
    imagen_paso = models.ImageField(upload_to='recetas_pics', blank=True, null=True)
    recetas = models.ForeignKey(ItemsPagina, on_delete=models.CASCADE)
    tiempo_preparacion = models.IntegerField()
    tiempo_coccion = models.IntegerField()

    def save(self, *args, **kwargs):
        if self.imagen_paso:
            try:
                # Abrir la imagen original
                img = Image.open(self.imagen_paso)
                img = img.resize((800, 600))  # Redimensionar la imagen si es necesario
                # Convertir la imagen a formato JPEG
                buffer = BytesIO()
                img.save(buffer, format='JPEG')
                buffer.seek(0)
                # Generar un nombre único para la imagen
                filename = os.path.join('recetas_pics', f"{uuid.uuid4()}.jpg")
                # Guardar la imagen en el sistema de archivos
                self.imagen_paso.save(filename, ContentFile(buffer.getvalue()), save=False)
                # Limpiar el buffer
                buffer.close()
            except Exception as e:
                print(f"Error al procesar la imagen: {e}")
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['numero']
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
