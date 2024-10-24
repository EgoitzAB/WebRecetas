from django.contrib import admin
from .models import Aparatos, Modelos, Categoria


class ModelosInline(admin.StackedInline):
    model = Modelos
    extra = 1

@admin.register(Aparatos)
class AparatosAdmin(admin.ModelAdmin):
    inlines = [ModelosInline]

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'imagen']
    search_fields = ['nombre']
