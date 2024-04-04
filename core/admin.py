from django.contrib import admin
from .models import ItemsPagina, Pasos, Ingredientes


class PasosInline(admin.TabularInline):
    model = Pasos
    extra = 1

class IngredientesInline(admin.TabularInline):
    model = Ingredientes
    extra = 1



class ItemsPaginaAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'fecha_creacion', 'fecha_modificacion', 'status']
    search_fields = ['titulo', 'contenido']
    list_filter = ['status', 'fecha_creacion', 'fecha_modificacion']
    inlines = [PasosInline, IngredientesInline]

admin.site.register(ItemsPagina, ItemsPaginaAdmin)

