from django.urls import path
from . import views
from django.views.decorators.cache import cache_page
from .sitemap import RecetasSitemap
app_name = 'core'

sitemaps ={
    'recetas': RecetasSitemap,
    }

urlpatterns = [
    path('', views.home, name='home'),
    path('receta_detalle/<slug:slug>/', views.VistaDetalle.as_view(), name='recetas'),
    path('search/', views.receta_search, name='receta_search'),
    path('autocomplete/', views.AutocompleteView.as_view(), name='autocomplete'),
    path('listado-recetas/', views.VistaLista.as_view(), name='receta_lista'),
]