from django.urls import path
from . import views
from .views import AutocompleteView

urlpatterns = [
    path('', views.home, name='home'),
    path('receta_detalle/', views.VistaDetalle.as_view(), name='recetas'),
    path('search/', views.receta_search, name='receta_search'),
    path('autocomplete/', AutocompleteView.as_view(), name='autocomplete'),
]