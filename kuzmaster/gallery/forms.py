from django import forms
from .models import CarBrand, CarModel

class FilterForm(forms.Form):
    """Форма фильтрации по марке и модели"""
    brand = forms.ModelChoiceField(
        queryset=CarBrand.objects.all(),
        required=False,
        empty_label="Все марки",
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'brand-select',
            'onchange': 'loadModels()'
        })
    )
    
    model = forms.ModelChoiceField(
        queryset=CarModel.objects.none(),
        required=False,
        empty_label="Все модели",
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'model-select'
        })
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'brand' in self.data and self.data['brand']:
            try:
                brand_id = int(self.data['brand'])
                self.fields['model'].queryset = CarModel.objects.filter(brand_id=brand_id)
            except (ValueError, TypeError):
                pass