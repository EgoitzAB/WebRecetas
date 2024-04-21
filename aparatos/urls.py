from django.urls import path
from . import views
from django.views.decorators.cache import cache_page
from .sitemap import AparatosSitemap


app_name = 'aparatos'

sitemaps ={
    'aparatos': AparatosSitemap,
    }

urlpatterns = [
    path('lista/', views.ListaAparatos.as_view(), name='aparatos_lista'),
    path('detalle/<slug:slug>', views.DetalleAparatos.as_view(), name='aparatos_detalle'),
]