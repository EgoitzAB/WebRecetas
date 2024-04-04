from django.shortcuts import render
from .models import ItemsPagina
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, TrigramSimilarity
from .forms import SearchForm
from django.views.generic import DetailView
from django.http import JsonResponse
from django.views import View
from django.db.models import Q


def home(request):
    recetas = ItemsPagina.objects.filter(status="CR")[:6]
    return render(request, 'core/home.html', {'recetas': recetas})

def receta_search(request):
    form = SearchForm()
    query = None
    results = []

    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            search_vector = SearchVector('titulo', weight='A', config='spanish')+ \
                SearchVector('nombre', weight='B', config='spanish')
            search_query = SearchQuery(query, config='spanish')
            results = ItemsPagina.publicado.annotate(
                similarity=TrigramSimilarity('titulo', query),
                #search=search_vector,
                #rank=SearchRank(search_vector, search_query)
                #).filter(rank__gte=0.3).order_by('-rank')
            ).filter(similarity__gt=0.1).order_by('-similarity')

    return render(request, 'core/receta_search.html',
                  {form: form, query: query, results: results})

class VistaDetalle(DetailView):
    model = ItemsPagina
    template_name = 'core/receta_detail.html'


class AutocompleteView(View):
    def get(self, request):
        query = request.GET.get('q', '')
        recetas = ItemsPagina.objects.filter(Q(nombre__trigram_similar=query) | Q(ingredientes__nombre__trigram_similar=query)).distinct()
        results = [{'id': receta.id, 'text': receta.nombre} for receta in recetas]
        return JsonResponse(results, safe=False)
