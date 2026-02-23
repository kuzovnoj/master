import logging
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse
from django.utils.http import urlencode
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.sessions.models import Session
import json

from .models import CarModel, Projection, Service, BodyPart, CalculationSession, SelectedPart

logger = logging.getLogger(__name__)

@ensure_csrf_cookie
def calculator_view(request, car_model_slug):
    """Основная страница калькулятора"""
    # Получаем модель авто
    car_model = get_object_or_404(CarModel, slug=car_model_slug)
    
    # Получаем или создаем сессию расчета
    if not request.session.session_key:
        request.session.save()
    
    session_key = request.session.session_key
    calculation_session, created = CalculationSession.objects.get_or_create(
        session_key=session_key,
        car_model=car_model
    )
    
    # Получаем все проекции для этой модели
    projections = car_model.projections.all()
    
    # Получаем все детали, сгруппированные по проекциям
    parts_by_projection = {}
    for projection in projections:
        parts_by_projection[projection.id] = projection.parts.filter(is_active=True)
    
    # Получаем все активные услуги
    services = Service.objects.filter(is_active=True)
    
    # Получаем выбранные детали для текущей сессии
    selected_parts = calculation_session.selected_parts.select_related('part', 'service').all()
    
    # Подготавливаем данные для JavaScript (координаты деталей)
    parts_data = []
    for projection in projections:
        for part in projection.parts.filter(is_active=True):
            parts_data.append({
                'id': part.id,
                'name': part.name,
                'projection_id': projection.id,
                'coordinates': part.coordinates
            })
    
    context = {
        'car_model': car_model,
        'projections': projections,
        'parts_by_projection': parts_by_projection,
        'services': services,
        'selected_parts': selected_parts,
        'total_price': calculation_session.get_total_price(),
        'parts_data_json': json.dumps(parts_data),
        'calculation_session': calculation_session,
    }
    
    return render(request, 'calculator/calculator.html', context)

@require_POST
def add_part_view(request):
    """Добавление детали в расчет"""
    print("=" * 50)
    print("add_part_view вызван!")
    print(f"Method: {request.method}")
    print(f"POST data: {request.POST}")
    print(f"Session key: {request.session.session_key}")
    
    part_id = request.POST.get('part_id')
    service_id = request.POST.get('service_id')
    
    print(f"part_id: {part_id}")
    print(f"service_id: {service_id}")
    
    if not part_id or not service_id:
        print("Ошибка: Не выбрана деталь или услуга")
        messages.error(request, 'Не выбрана деталь или услуга')
        return redirect(request.META.get('HTTP_REFERER', '/calculator/sedan/'))
    
    # Получаем сессию
    if not request.session.session_key:
        request.session.save()
        print(f"Новая сессия создана: {request.session.session_key}")
    
    session_key = request.session.session_key
    print(f"Session key: {session_key}")
    
    try:
        part = BodyPart.objects.get(id=part_id, is_active=True)
        service = Service.objects.get(id=service_id, is_active=True)
        print(f"Найдена деталь: {part.name}")
        print(f"Найдена услуга: {service.name}")
        
        # Получаем сессию расчета
        calculation_session, created = CalculationSession.objects.get_or_create(
            session_key=session_key,
            car_model=part.projection.car_model
        )
        print(f"Сессия расчета: {'создана' if created else 'существует'}, id: {calculation_session.id}")
        
        # Создаем или обновляем выбранную деталь
        selected_part, created = SelectedPart.objects.update_or_create(
            session=calculation_session,
            part=part,
            defaults={
                'service': service,
                'price': service.price
            }
        )
        
        if created:
            messages.success(request, f'Деталь "{part.name}" добавлена в расчет')
            print(f"Деталь добавлена: {selected_part.id}")
        else:
            messages.success(request, f'Услуга для детали "{part.name}" обновлена')
            print(f"Деталь обновлена: {selected_part.id}")
            
        print(f"Перенаправление на: {part.projection.car_model.slug}")
        return redirect('calculator:calculator', car_model_slug=part.projection.car_model.slug)
            
    except BodyPart.DoesNotExist:
        print(f"Ошибка: Деталь с id {part_id} не найдена")
        messages.error(request, 'Деталь не найдена')
    except Service.DoesNotExist:
        print(f"Ошибка: Услуга с id {service_id} не найдена")
        messages.error(request, 'Услуга не найдена')
    except CalculationSession.DoesNotExist as e:
        print(f"Ошибка сессии: {e}")
        messages.error(request, 'Ошибка при создании сессии')
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")
        import traceback
        traceback.print_exc()
        messages.error(request, f'Ошибка: {str(e)}')
    
    return redirect(request.META.get('HTTP_REFERER', '/calculator/sedan/'))

@require_POST
def remove_part_view(request, selected_part_id):
    """Удаление детали из расчета"""
    try:
        selected_part = SelectedPart.objects.get(id=selected_part_id)
        car_model_slug = selected_part.part.projection.car_model.slug
        part_name = selected_part.part.name
        
        # Проверяем, принадлежит ли деталь текущей сессии
        if request.session.session_key and selected_part.session.session_key == request.session.session_key:
            selected_part.delete()
            messages.success(request, f'Деталь "{part_name}" удалена из расчета')
        else:
            messages.error(request, 'Нет прав для удаления этой детали')
            
    except SelectedPart.DoesNotExist:
        messages.error(request, 'Деталь не найдена')
        car_model_slug = 'sedan'  # Значение по умолчанию
    
    return redirect('calculator:calculator', car_model_slug=car_model_slug)

@require_POST
def update_service_view(request, selected_part_id):
    """Обновление услуги для выбранной детали"""
    service_id = request.POST.get('service_id')
    
    if not service_id:
        messages.error(request, 'Не выбрана услуга')
        return redirect(request.META.get('HTTP_REFERER', 'calculator:calculator'))
    
    try:
        selected_part = SelectedPart.objects.get(id=selected_part_id)
        service = Service.objects.get(id=service_id, is_active=True)
        car_model_slug = selected_part.part.projection.car_model.slug
        
        # Проверяем, принадлежит ли деталь текущей сессии
        if request.session.session_key and selected_part.session.session_key == request.session.session_key:
            selected_part.service = service
            selected_part.price = service.price
            selected_part.save()
            messages.success(request, f'Услуга для детали "{selected_part.part.name}" обновлена')
        else:
            messages.error(request, 'Нет прав для изменения этой детали')
            
    except (SelectedPart.DoesNotExist, Service.DoesNotExist):
        messages.error(request, 'Ошибка при обновлении услуги')
        car_model_slug = 'sedan'
    
    return redirect('calculator:calculator', car_model_slug=car_model_slug)