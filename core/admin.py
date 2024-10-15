from django.contrib import admin
from .models import ItemsPagina, Pasos, Ingredientes, FondosHeaders, Categoria

class PasosInline(admin.TabularInline):
    model = Pasos
    extra = 1

class IngredientesInline(admin.TabularInline):
    model = Ingredientes
    extra = 1

class ItemsPaginaAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'fecha_creacion', 'fecha_modificacion', 'status', 'slug']
    search_fields = ['titulo', 'contenido']
    list_filter = ['status', 'fecha_creacion', 'fecha_modificacion']
    inlines = [PasosInline, IngredientesInline]
    # Esto añade el campo 'categoria' al formulario de admin
    raw_id_fields = ['categoria']

class FondosHeadersAdmin(admin.ModelAdmin):
    list_display = ['vista', 'fecha_creacion']
    search_fields = ['vista']
    list_filter = ['fecha_creacion']

class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'imagen']
    search_fields = ['nombre']

admin.site.register(ItemsPagina, ItemsPaginaAdmin)
admin.site.register(FondosHeaders, FondosHeadersAdmin)
admin.site.register(Categoria, CategoriaAdmin)

