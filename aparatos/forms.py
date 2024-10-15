from django import forms
from .models import Aparatos, Categoria


class AparatosForm(forms.ModelForm):
    categorias = forms.MultipleChoiceField(choices=[], required=False, widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Aparatos
        fields = ('categorias',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['categorias'].choices = [(c.id, c.nombre) for c in Categoria.objects.all()]

    def filter(self, queryset):  # Cambia el nombre del método de filter_recetas a filter
        categoria = self.cleaned_data.get('categorias')

        if categoria:
            queryset = queryset.filter(categoria=categoria)

        return queryset