from django.db import models
from django.contrib.auth.models import User
from easy_thumbnails.fields import ThumbnailerImageField
from django.utils.text import slugify
from autoslug import AutoSlugField
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from taggit.managers import TaggableManager


class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre


class Aparatos(models.Model):
    class Status(models.TextChoices):
        CREADO = 'CR', 'Creado'
        PUBLICADO = 'PB', 'Publicado'

    nombre = models.CharField(max_length=250)
    descripcion = models.TextField()
    usos = models.TextField()
    caracteristica_generales = models.TextField()
    imagen = ThumbnailerImageField(upload_to='pasos_pics', blank=True, null=True)
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.CREADO)
    slug = AutoSlugField(unique=True, populate_from='nombre')
    tags = TaggableManager(blank=True)
    categoria = models.ManyToManyField(Categoria, blank=True)

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


class Modelos(models.Model):
    class Status(models.TextChoices):
        CREADO = 'CR', 'Creado'
        PUBLICADO = 'PB', 'Publicado'

    nombre = models.CharField(max_length=255)
    modelo = models.ForeignKey(Aparatos, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name='aparatos_likes', blank=True)
    link_amazon = models.URLField(blank=True)
    caracteristicas_modelo = models.TextField()
    año = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.CREADO)
    imagen = ThumbnailerImageField(upload_to='pasos_pics', blank=True, null=True)
    slug = AutoSlugField(unique=True, populate_from='nombre')
    tags = TaggableManager(blank=True)
    fecha_modificacion = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            # Generar el slug basado en el nombre del aparato y del modelo
            self.slug = slugify(f"{self.modelo.nombre}-{self.nombre}")

        # Resto de la lógica del método save
        super().save(*args, **kwargs)

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
