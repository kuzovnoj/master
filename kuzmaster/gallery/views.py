from django.shortcuts import render
from django.http import JsonResponse
from .models import CarBrand, CarModel, GalleryImage
from .forms import FilterForm

def gallery_view(request):
    """Главная страница галереи"""
    # Получаем параметры фильтрации
    brand_id = request.GET.get('brand')
    model_id = request.GET.get('model')
    
    # Базовый queryset
    images = GalleryImage.objects.filter(is_active=True).select_related(
        'car_model', 'car_model__brand'
    )
    
    # Применяем фильтры
    if model_id:
        images = images.filter(car_model_id=model_id)
    elif brand_id:
        images = images.filter(car_model__brand_id=brand_id)
    
    # Берем первые 12 изображений (можно настроить пагинацию)
    images = images[:12]
    
    # Форма фильтрации
    form = FilterForm(request.GET or None)
    
    context = {
        'title': 'Галерея работ',
        'images': images,
        'form': form,
        'selected_brand': brand_id,
        'selected_model': model_id,
    }
    return render(request, 'gallery/gallery.html', context)

def load_models(request):
    """AJAX запрос для загрузки моделей по выбранной марке"""
    brand_id = request.GET.get('brand_id')
    if brand_id:
        models = CarModel.objects.filter(brand_id=brand_id).order_by('name')
        data = [{'id': model.id, 'name': model.name} for model in models]
        return JsonResponse(data, safe=False)
    return JsonResponse([], safe=False)