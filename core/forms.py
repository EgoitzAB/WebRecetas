from django import forms


class SearchForm(forms.Form):
    query = forms.CharField()


class ItemsPaginaForm(forms.Form):
    CATEGORIAS_CHOICES = [
        ('', 'Todas las categorías'),  # Opción por defecto para mostrar todas las categorías
        ('car', 'Carne'),
        ('pes', 'Pescado'),
        ('ave', 'Ave'),
        ('cal', 'Caldo'),
        ('ens', 'Ensalada'),
        ('pas', 'Pasta'),
        ('pos', 'Postre'),
        ('sop', 'Sopa'),
        ('ver', 'Verdura'),
        ('otr', 'Otro'),
    ]

    categoria = forms.ChoiceField(choices=CATEGORIAS_CHOICES, required=False)

    def filter_recetas(self, queryset):
        categoria = self.cleaned_data.get('categoria')

        if categoria:
            queryset = queryset.filter(categoria=categoria)

        return queryset
