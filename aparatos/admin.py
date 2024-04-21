from django.contrib import admin
from .models import Aparatos, Modelos, Categoria


class ModelosInline(admin.StackedInline):
    model = Modelos
    extra = 1

@admin.register(Aparatos)
class AparatosAdmin(admin.ModelAdmin):
    inlines = [ModelosInline]
