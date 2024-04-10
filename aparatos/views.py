from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Aparatos
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
            queryset = form.filter_recetas(queryset)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = Aparatos(self.request.GET)
        return context


class DetalleAparatos(DetailView):
    model = Aparatos
    template_name = 'aparatos/aparatos_detalle.html'
    context_object_name = 'aparatos_detalle.html'