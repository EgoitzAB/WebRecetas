import os
import json
from core.models import ItemsPagina, Pasos, Ingredientes, Categoria
from django.contrib.auth.models import User
from django.core.files import File
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Carga recetas desde un archivo JSON'

    def handle(self, *args, **options):
        current_dir = os.path.dirname(__file__)
        json_file_path = os.path.join(current_dir, 'recetas_completas.json')
        IMAGENES_DIR = os.path.join(current_dir, 'imagenes')
        # Cargar el archivo JSON
        with open(json_file_path, 'r') as file:
            recetas_json = json.load(file)

        # Llamar a la función para cargar los datos
        self.cargar_recetas(recetas_json, IMAGENES_DIR)


    def save_local_image(self, model_instance, image_url, image_field_name, IMAGENES_DIR):
        # Guardar la imagen sin parámetros
        image_filename = image_url.split('/')[-1].split('?')[0]  # Quitar parámetros al guardar
        # Buscar la imagen con parámetros
        image_path = os.path.join(IMAGENES_DIR, image_url.split('/')[-1])  # Mantener la URL completa para la búsqueda
        
        print(f"Buscando imagen en: {image_path}")  # Debugging
        
        # Verificar si la imagen existe
        if os.path.exists(image_path):
            with open(image_path, 'rb') as img_file:
                getattr(model_instance, image_field_name).save(image_filename, File(img_file), save=False)
                print(f"Imagen guardada: {image_filename}")  # Confirmación
        else:
            print(f"Imagen no encontrada: {image_url.split('/')[-1]}")  # Mensaje de error
        
    # Función para procesar las recetas
    def cargar_recetas(self, recetas_json, images_dir):
        # Iterar sobre cada receta en el JSON
        for receta in recetas_json:
            # Verificar si la categoría ya existe o crearla
            categoria, _ = Categoria.objects.get_or_create(nombre="General")

            # Crear la receta principal (ItemsPagina)
            nueva_receta = ItemsPagina.objects.create(
                titulo=receta['title'],
                autor=receta['author'],
                contenido=receta['descripcion'],
                categoria=categoria,
                status=ItemsPagina.Status.PUBLICADO,  # Asigna como 'Publicado'
            )

            # Asignar la primera imagen al campo imagen si está disponible
            if receta['images']:
                # Guardar la imagen localmente en el campo de la receta
                self.save_local_image(nueva_receta, receta['images'][0], 'imagen', images_dir)

            # Guardar la receta para que tengamos una ID
            nueva_receta.save()

            # Crear los ingredientes
            for ingrediente in receta['ingredients']:
                Ingredientes.objects.create(
                    nombre=ingrediente,
                    recetas=nueva_receta
                )

            # Crear los pasos
            for i, paso in enumerate(receta['preparation']):
                nuevo_paso = Pasos.objects.create(
                    numero=i + 1,
                    descripcion=paso['step'],
                    recetas=nueva_receta,
                    tiempo_preparacion=receta['tiempo_pre'],  # Suponiendo que cada paso toma igual tiempo
                    tiempo_coccion=receta['tiempo_coc'],  # Si necesitas agregar tiempo de cocción
                )

                # Asignar imagen si está disponible en el paso
                if 'image' in paso:
                    self.save_local_image(nuevo_paso, paso['image'], 'imagen_paso', images_dir)

                # Guardamos el paso en la base de datos
                nuevo_paso.save()
