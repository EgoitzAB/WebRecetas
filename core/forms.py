from django import forms
from .models import Categoria, ItemsPagina

class SearchForm(forms.Form):
    query = forms.CharField()

class ItemsPaginaForm(forms.Form):
    categorias = forms.MultipleChoiceField(choices=[], required=False, widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = ItemsPagina
        fields = ('categorias',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['categorias'].choices = [(c.id, c.nombre) for c in Categoria.objects.all()]

    def filter_recetas(self, queryset):
        categoria = self.cleaned_data.get('categoria')

        if categoria:
            # Filtrar el queryset utilizando el objeto de categoría
            queryset = queryset.filter(categoria=categoria)

        return queryset


