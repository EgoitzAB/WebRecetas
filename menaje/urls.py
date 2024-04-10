from django.urls import path
from . import views
from django.views.decorators.cache import cache_page

app_name = 'menaje'

urlpatterns = [
    path('lista/', views.ListaMenaje.as_view(), name='menaje_lista'),
    path('detalle/', views.DetalleMenaje.as_view(), name='menaje_detalle'),
]