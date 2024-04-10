from django import forms
from .models import Aparatos, Categoria


class AparatosForm(forms.ModelForm):
    categorias = forms.MultipleChoiceField(choices=[], required=False, widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Aparatos
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['categorias'].choices = [(c.id, c.nombre) for c in Categoria.objects.all()]


