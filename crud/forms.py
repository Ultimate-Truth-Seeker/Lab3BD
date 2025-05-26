from django import forms
from django.forms.models import inlineformset_factory
from .models import Product, ProductTag, Tag, CategoryChoices, StatusChoices

class ProductForm(forms.ModelForm):
    status = forms.ChoiceField(
        choices=StatusChoices.choices,
        widget=forms.Select(),
        label="Status"
    )
    category = forms.ChoiceField(
        choices=CategoryChoices.choices,
        widget=forms.Select(),
        label="Category"
    )

    class Meta:
        model  = Product
        fields = ['name', 'sku', 'status', 'category']

# FormSet para la tabla intermedia, permitirá múltiples tags + relevance
ProductTagFormSet = inlineformset_factory(
    Product,
    ProductTag,
    fields     = ['tag', 'relevance'],
    extra      = 1,
    can_delete = True,
    min_num    = 1,
    validate_min = True,
    widgets = {
      'tag':       forms.Select(choices=Tag.objects),
      'relevance': forms.NumberInput(attrs={'min':1, 'max':10}),
    }
)