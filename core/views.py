from django.shortcuts import render
from .models import ItemsPagina
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, TrigramSimilarity
from .forms import SearchForm, ItemsPaginaForm
from django.views.generic import DetailView, ListView
from django.http import JsonResponse
from django.views import View
from django.db.models import Q
from django.views.decorators.cache import cache_page
from django.conf import settings
from .utils import obtener_vistas_de_receta, recetas_mas_vistas
import redis


@cache_page(60 * 15)
def home(request):
    # Obtener las recetas más vistas utilizando la función recetas_mas_vistas
    recetas_destacadas = recetas_mas_vistas(request, cantidad_recetas=6)

    # Obtener las recetas distintas y las recetas normales
    recetas_distintas = ItemsPagina.objects.filter(status='CR').order_by('categoria').distinct('categoria')
    recetas = ItemsPagina.objects.filter(status="CR")[:6]

    # Obtener el número de vistas de cada receta
    for receta in recetas_destacadas:
        receta.num_vistas = obtener_vistas_de_receta(receta.id)

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
        # Actualizar el conjunto recetas_vistas con la nueva puntuación
        redis_connection.zadd('recetas_vistas', {obj.id: num_vistas})
        return obj



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
