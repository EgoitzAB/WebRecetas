from django.db import models
from easy_thumbnails.fields import ThumbnailerImageField
from autoslug import AutoSlugField
from taggit.managers import TaggableManager
from django.utils.text import slugify
from django.contrib.auth.models import User
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre


class Menaje(models.Model):
    class Status(models.TextChoices):
        CREADO = 'CR', 'Creado'
        PUBLICADO = 'PB', 'Publicado'

    nombre = models.CharField(max_length=200)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    descripcion = models.TextField()
    usos = models.CharField(max_length=500)
    link_amazon = models.URLField(blank=True)
    slug = AutoSlugField(unique=True, populate_from='nombre')
    imagen = ThumbnailerImageField(upload_to='pasos_pics', blank=True, null=True)
    tags = TaggableManager(blank=True)
    likes = models.ManyToManyField(User, related_name='menaje_likes', blank=True)
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.CREADO)
    categoria = models.ManyToManyField(Categoria)

    def save(self, *args, **kwargs):
            if not self.slug:
                self.slug = slugify(self.nombre)

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