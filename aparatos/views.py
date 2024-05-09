from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
from .models import Aparatos, Modelos
from core.models import FondosHeaders
from .forms import AparatosForm
# Create your views here.

class ListaAparatos(ListView):
    model = Aparatos
    template_name = 'aparatos/aparatos_lista.html'
    context_object_name = 'aparatos'
    paginate_by = 9

    def get_queryset(self):
        queryset = Aparatos.objects.filter(status='CR').order_by('categoria')
        form = AparatosForm(self.request.GET)
        if form.is_valid():
            categorias_selected = form.cleaned_data.get('categorias')
            if categorias_selected:
                queryset = queryset.filter(categoria__in=categorias_selected)
        return queryset


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            imagen_fondo = cache.get_or_set('imagen_fondo_lista_aparatos', FondosHeaders.objects.get(vista="aparatos_lista").imagen_fondo, timeout=6)
        except ObjectDoesNotExist:
            # Si el objeto FondosHeaders no existe, proporciona un valor predeterminado o maneja la excepción de otra manera
            imagen_fondo = '/home/felipe/Recetas/media/imagenes_fondo/kitchen-2400367_1920.jpg'  # Cambia esto por la ruta de tu imagen predeterminada
        context['form'] = AparatosForm(self.request.GET)
        context['imagen_fondo'] = imagen_fondo
        return context

class DetalleAparatos(DetailView):
    model = Aparatos
    template_name = 'aparatos/aparatos_detalle.html'
    context_object_name = 'aparatos'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            imagen_fondo = cache.get_or_set('imagen_fondo_detalle_aparatos', FondosHeaders.objects.get(vista="aparatos_detalle").imagen_fondo, timeout=6)
        except ObjectDoesNotExist:
            # Si el objeto FondosHeaders no existe, proporciona un valor predeterminado o maneja la excepción de otra manera
            imagen_fondo = '/home/felipe/Recetas/media/imagenes_fondo/kitchen-2400367_1920.jpg'  # Cambia esto por la ruta de tu imagen predeterminada
        context['imagen_fondo'] = imagen_fondo
        return context


class DetalleModelo(DetailView):
    model = Modelos
    template_name = 'aparatos/modelos_detalle.html'
    context_object_name = 'modelos'