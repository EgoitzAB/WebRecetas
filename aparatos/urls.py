from django.urls import path
from . import views
from django.views.decorators.cache import cache_page

app_name = 'aparatos'

urlpatterns = [
    path('lista/', views.ListaAparatos.as_view(), name='aparatos_lista'),
    path('detalle/', views.DetalleAparatos.as_view(), name='aparatos_detalle'),
]