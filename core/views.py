from typing import Any
from django.shortcuts import render, get_object_or_404
from .models import ItemsPagina, FondosHeaders
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, TrigramSimilarity
from .forms import SearchForm, ItemsPaginaForm
from django.views.generic import DetailView, ListView
from django.http import JsonResponse
from django.views import View, generic
from django.db.models import Q, Count, F
from django.views.decorators.cache import cache_page
from django.core.exceptions import ObjectDoesNotExist
from django.core.cache import cache
from django.conf import settings
from django.template.response import TemplateResponse
from .utils import obtener_vistas_de_receta, recetas_mas_vistas, funcion_visitas
from .recomendador import RecetaRecomendador, RecetaHistorial
import redis


def home(request):
    # Recuperar imagen del fondo de pantalla
    try:
        imagen_fondo = cache.get_or_set('imagen_fondo_home', FondosHeaders.objects.get(vista="home").imagen_fondo, timeout=6)
    except ObjectDoesNotExist:
        # Manejar el caso en el que no hay ningún objeto en la base de datos
        imagen_fondo = 'www/WebRecetas/media/imagenes_fondo/pasta-1181189_1920_eztJu4l.jpg'
    # Recuperar las vistas de la página desde el caché
    contadores_visitas = funcion_visitas()
    visitas_totales = contadores_visitas.get('visitas_totales', 0)
    visitas_sesion = contadores_visitas.get('visitas_sesion', 0)
    # Recuperar las recetas del cache y renderizar, o hacer queries y generar cache
    recetas_home = cache.get_many(['recetas', 'recetas_distintas', 'recetas_destacadas'])
    if recetas_home:
        return render(request, 'core/home.html', {'recetas': recetas_home['recetas'],
                                                    'recetas_distintas': recetas_home['recetas_distintas'],
                                                    'recetas_destacadas': recetas_home['recetas_destacadas'],
                                                    'imagen_fondo': imagen_fondo,
                                                    'visitas_totales': visitas_totales,
                                                    'visitas_sesion': visitas_sesion,
                                                    })
    else:
        # Obtener las recetas más vistas utilizando la función recetas_mas_vistas
        recetas_destacadas = recetas_mas_vistas(request, cantidad_recetas=6)
        # Obtener el número de vistas de cada receta
        for receta in recetas_destacadas:
            receta.num_vistas = obtener_vistas_de_receta(receta.id)
        recetas = ItemsPagina.objects.filter(status='PB')
        #Agrupar las recetas por categoría y seleccionar una receta representativa de cada categoría
        recetas_distintas = []
        categorias_distintas = set()  # Usamos un conjunto para mantener las categorías únicas
        for receta in recetas:
            if receta.categoria not in categorias_distintas:
                # Contar el número de recetas por categoría
                num_recetas = recetas.filter(categoria=receta.categoria).count()
                # Asignar el número de recetas al objeto receta
                receta.num_recetas = num_recetas
                recetas_distintas.append(receta)
                categorias_distintas.add(receta.categoria)

        timeout = 180 # ajustando el timeout del caché a 3 minutos
        cache.set_many({'recetas': recetas, 'recetas_distintas': recetas_distintas,
                    'recetas_destacadas': recetas_destacadas},
                    timeout=timeout)
        return render(request, 'core/home.html', {'recetas': recetas,
                                                'recetas_distintas': recetas_distintas,
                                                'recetas_destacadas': recetas_destacadas,
                                                'imagen_fondo': imagen_fondo,
                                                'visitas_totales': visitas_totales,
                                                'visitas_sesion': visitas_sesion})

def receta_search(request):
    form = SearchForm()
    query = None
    results = []

    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            search_vector = SearchVector('titulo', weight='A', config='spanish') + \
                SearchVector('ingredientes__nombre', weight='B', config='spanish') + \
                SearchVector('pasos__contenido', weight='C', config='spanish')
            search_query = SearchQuery(query, config='spanish')
            results = ItemsPagina.objects.filter(status='CR').annotate(
                similarity=TrigramSimilarity(search_vector, search_query),  # Ajustado para usar search_vector y search_query
            ).filter(similarity__gt=0.5).order_by('-similarity')

    return render(request, 'core/receta_search.html',
                    {'form': form, 'query': query, 'results': results})


class VistaLista(ListView):
    model = ItemsPagina
    template_name = 'core/receta_lista.html'
    context_object_name = 'recetas'
    paginate_by = 6

    def get_queryset(self):
        queryset = ItemsPagina.objects.filter(status='PB').order_by('categoria')
        form = ItemsPaginaForm(self.request.GET)
        if form.is_valid():
            categorias_selected = form.cleaned_data.get('categorias')
            if categorias_selected:
                queryset = queryset.filter(categoria__in=categorias_selected)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            imagen_fondo = cache.get_or_set('imagen_fondo_lista_recetas', FondosHeaders.objects.get(vista="recetas_lista").imagen_fondo, timeout=6)
        except ObjectDoesNotExist:
            # Si el objeto FondosHeaders no existe, proporciona un valor predeterminado o maneja la excepción de otra manera
            imagen_fondo = '/home/felipe/Recetas/media/imagenes_fondo/kitchen-2400367_1920.jpg'  # Cambia esto por la ruta de tu imagen predeterminada
        context['imagen_fondo'] = imagen_fondo
        context['form'] = ItemsPaginaForm(self.request.GET)
        return context


def render_to_response(self, context, **response_kwargs):
    # Generar una clave única para esta página basada en la URL y los parámetros de consulta
    cache_key = 'vista_lista_cache_' + self.request.get_full_path()

    # Intentar recuperar la página renderizada desde la caché
    cached_response = cache.get(cache_key)

    if cached_response is None:
        # Si la página no está en caché, renderizarla y almacenarla en caché
        response = TemplateResponse(request=self.request, template=self.template_name, context=context)
        rendered_content = response.render()
        cache.set(cache_key, rendered_content, timeout=300)  # Caché durante 5 minutos
        return response

    # Si la página está en caché, devolverla directamente
    return render(self.request, self.template_name, {'content': cached_response})


class VistaDetalle(DetailView):
    model = ItemsPagina
    template_name = 'core/receta_detalle.html'
    slug_field = 'slug'
    slug_url_kwargs = 'slug'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        # Incrementar el contador de vistas utilizando Redis
        redis_connection = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)
        redis_connection.incr(f"receta:{obj.id}:vistas")
        # Obtener el número total de vistas de esta receta
        num_vistas = redis_connection.get(f"receta:{obj.id}:vistas")
        print(f"Número total de vistas de la receta {obj.id}: {num_vistas}")
        # Actualizar el conjunto recetas_vistas con la nueva puntuación
        redis_connection.zadd('recetas_vistas', {obj.id: num_vistas})
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Obtener el receta_id
        receta = self.get_object()
        # Pasar el receta_id al middleware
        historial = RecetaHistorial(self.request)
        historial.añadir(receta)
        # Obtener recomendaciones de recetas
        recomendador = RecetaRecomendador()
        recetas_recomendadas_ids = recomendador.sugerir_recetas_para(historial, 4)
        recetas_recomendadas = ItemsPagina.objects.filter(id__in=recetas_recomendadas_ids)
        categoria = receta.categoria
        if categoria:
            context['categoria'] = categoria
        print(recetas_recomendadas)
        print(recetas_recomendadas_ids)
        print(categoria)
        context['recetas_recomendadas'] = recetas_recomendadas

        return context


class AutocompleteView(View):
    def get(self, request):
        query = request.GET.get('q', '')

        # Realizar la búsqueda utilizando múltiples vectores de similitud trigram
        recetas = ItemsPagina.objects.annotate(
            similarity_titulo=TrigramSimilarity('titulo', query),
            similarity_pasos=TrigramSimilarity('pasos__descripcion', query),
            similarity_ingredientes=TrigramSimilarity('ingredientes__nombre', query)
        ).filter(
            Q(similarity_titulo__gt=0.2) |
            Q(similarity_pasos__gt=0.1) |
            Q(similarity_ingredientes__gt=0.1)
        ).values('id', 'slug', 'titulo').distinct()

        # Se pasa el slug y el título de las recetas a la librería JavaScript Select2
        results = [{'id': receta['slug'], 'text': receta['titulo']} for receta in recetas]

        return JsonResponse(results, safe=False)


class TermsOfUseView(generic.TemplateView):
    template_name = 'core/terminos_de_uso.html'


class PrivacidadView(generic.TemplateView):
    template_name = 'core/privacidad.html'
