from django.shortcuts import render
from django.db.models import Prefetch
from .models import WorkCategory, PriceItem
from kuzov.utils import DataMixin

def price_list_view(request):
    """Страница прайс-листа"""
    categories = WorkCategory.objects.filter(is_active=True).prefetch_related(
        Prefetch(
            'price_items',
            queryset=PriceItem.objects.filter(is_active=True).select_related('part').order_by('part__order'),
            to_attr='items'
        )
    ).order_by('order')

    mixin = DataMixin()
    base_context = mixin.extra_context

    context = {
        'title': 'Прайс-лист',
        'categories': categories,
    }

    union_context = {**context, **base_context}

    return render(request, 'works/price_list.html', union_context)