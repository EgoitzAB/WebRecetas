from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Menaje
from .forms import MenajeForm
# Create your views here.

class ListaMenaje(ListView):
    model = Menaje
    template_name = 'menaje/menaje_lista.html'
    context_object_name = 'menaje'
    paginate_by = 9

    def get_queryset(self):
        queryset = Menaje.objects.filter(status='CR').order_by('categoria')
        form = MenajeForm(self.request.GET)
        if form.is_valid():
            queryset = form.filter_recetas(queryset)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = Menaje(self.request.GET)
        return context


class DetalleMenaje(DetailView):
    model = Menaje
    template_name = 'menaje/detalle.html'
    context_object_name = 'menaje_detalle.html'