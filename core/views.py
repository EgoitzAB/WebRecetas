from typing import Any
from django.shortcuts import render, get_object_or_404
from .models import ItemsPagina
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, TrigramSimilarity
from .forms import SearchForm, ItemsPaginaForm
from django.views.generic import DetailView, ListView
from django.http import JsonResponse
from django.views import View, generic
from django.db.models import Q
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from django.conf import settings
from django.template.response import TemplateResponse
from .utils import obtener_vistas_de_receta, recetas_mas_vistas
from .recomendador import RecetaRecomendador, RecetaHistorial
import redis


def home(request):
    #Recuperar las recetas del cache y renderizar, o hacer queries y generar cache
    recetas_home = cache.get_many(['recetas', 'recetas_distintas', 'recetas_destacadas'])
    if recetas_home:
        return render(request, 'core/home.html', {'recetas': recetas_home['recetas'],
                    'recetas_distintas' : recetas_home['recetas_distintas'],
                    'recetas_destacadas': recetas_home['recetas_destacadas']})
    else:
        # Obtener las recetas más vistas utilizando la función recetas_mas_vistas
        recetas_destacadas = recetas_mas_vistas(request, cantidad_recetas=6)
        # Obtener las recetas distintas y las recetas normales
        # Agrupar las recetas por categoría y seleccionar una receta representativa de cada categoría
        recetas_distintas = []
        categorias_distintas = set()  # Usamos un conjunto para mantener las categorías únicas
        for receta in ItemsPagina.objects.filter(status='CR'):
            if receta.categoria not in categorias_distintas:
                recetas_distintas.append(receta)
                categorias_distintas.add(receta.categoria)
        recetas = ItemsPagina.objects.filter(status="CR")[:6]
        # Obtener el número de vistas de cada receta
        for receta in recetas_destacadas:
            receta.num_vistas = obtener_vistas_de_receta(receta.id)

        timeout = 180 # ajustando el timeout del caché a 3 minutos
        cache.set_many({'recetas': recetas, 'recetas_distintas': recetas_distintas,
                    'recetas_destacadas': recetas_destacadas},
                    timeout=timeout)
        return render(request, 'core/home.html', {'recetas': recetas, 'recetas_distintas': recetas_distintas, 'recetas_destacadas': recetas_destacadas})

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
        queryset = ItemsPagina.objects.filter(status='CR').order_by('categoria')
        form = ItemsPaginaForm(self.request.GET)
        if form.is_valid():
            queryset = form.filter_recetas(queryset)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
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
        print(recetas_recomendadas)
        print(recetas_recomendadas_ids)
        context['recetas_recomendadas'] = recetas_recomendadas

        return context


class AutocompleteView(View):
    def get(self, request):
        query = request.GET.get('q', '')
        recetas = ItemsPagina.objects.filter(
            Q(titulo__trigram_similar=query) |
            Q(pasos__descripcion__trigram_similar=query) |
            Q(ingredientes__nombre__trigram_similar=query)
        ).distinct()
        # Se pasa el slug a la librería javascript select
        results = [{'id': receta.slug, 'text': receta.titulo, } for receta in recetas]
        print(results)
        return JsonResponse(results, safe=False)


class TermsOfUseView(generic.TemplateView):
    template_name = 'core/terminos_de_uso.html'


class PrivacidadView(generic.TemplateView):
    template_name = 'core/privacidad.html'
