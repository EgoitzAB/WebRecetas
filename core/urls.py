from django.urls import path
from . import views
from django.views.decorators.cache import cache_page
from .sitemap import RecetasSitemap
from aparatos.sitemap import AparatosSitemap

app_name = 'core'

sitemaps ={
    'recetas': RecetasSitemap,
    'aparatos': AparatosSitemap,
    }

urlpatterns = [
    path('', views.home, name='home'),
    path('receta_detalle/<slug:slug>/', views.VistaDetalle.as_view(), name='recetas'),
    path('search/', views.receta_search, name='receta_search'),
    path('autocomplete/', views.AutocompleteView.as_view(), name='autocomplete'),
    path('listado-recetas/', views.VistaLista.as_view(), name='receta_lista'),
    path('terminos-de-uso/', views.TermsOfUseView.as_view(), name='terms_of_use'),
    path('politica-de-privacidad/', views.PrivacidadView.as_view(), name='privacy_policy'),
    path('favorito/agregar/<int:receta_id>/', views.agregar_favorito, name='agregar_favorito'),
    path('favorito/eliminar/<int:receta_id>/', views.eliminar_favorito, name='eliminar_favorito'),
    path('perfil/', views.perfil_usuario, name='perfil_usuario'),
]