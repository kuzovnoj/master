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

from .models import CarModel, Projection, Service, BodyPart, CalculationSession, SelectedPart, PartService

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
    
    # Подготавливаем данные для JavaScript (координаты деталей и доступные услуги с ценами)
    parts_data = []
    for projection in projections:
        for part in projection.parts.filter(is_active=True):
            # Получаем доступные услуги для этой детали с их ценами
            part_services = part.part_services.filter(is_active=True).select_related('service')
            services_for_part = []
            for ps in part_services:
                services_for_part.append({
                    'id': ps.service.id,
                    'name': ps.service.name,
                    'price': str(ps.price),
                    'color': ps.service.color  # ДОБАВЛЯЕМ ЦВЕТ
                })
            
            parts_data.append({
                'id': part.id,
                'name': part.name,
                'projection_id': projection.id,
                'coordinates': part.coordinates,
                'services': services_for_part
            })
    
    context = {
        'car_model': car_model,
        'projections': projections,
        'parts_by_projection': parts_by_projection,
        'services': services,
        'selected_parts': selected_parts,
        'total_price': calculation_session.get_total_price(),
        'parts_data_json': json.dumps(parts_data, ensure_ascii=False),
        'calculation_session': calculation_session,
    }
    
    return render(request, 'calculator/calculator.html', context)

@require_POST
def add_part_view(request):
    """Добавление детали в расчет"""
    part_id = request.POST.get('part_id')
    service_id = request.POST.get('service_id')
    
    if not part_id or not service_id:
        messages.error(request, 'Не выбрана деталь или услуга')
        return redirect(request.META.get('HTTP_REFERER', '/calculator/sedan/'))
    
    # Получаем сессию
    if not request.session.session_key:
        request.session.save()
    
    session_key = request.session.session_key
    
    try:
        part = BodyPart.objects.get(id=part_id, is_active=True)
        
        # Получаем цену из PartService, а не из базовой услуги
        try:
            part_service = PartService.objects.get(
                part=part,
                service_id=service_id,
                is_active=True
            )
            price = part_service.price
            service = part_service.service
        except PartService.DoesNotExist:
            messages.error(request, f'Услуга не доступна для этой детали')
            return redirect('calculator:calculator', car_model_slug=part.projection.car_model.slug)
        
        # Получаем сессию расчета
        calculation_session, created = CalculationSession.objects.get_or_create(
            session_key=session_key,
            car_model=part.projection.car_model
        )
        
        # Создаем или обновляем выбранную деталь
        selected_part, created = SelectedPart.objects.update_or_create(
            session=calculation_session,
            part=part,
            defaults={
                'service': service,
                'price': price  # Используем цену из PartService
            }
        )
        
        if created:
            messages.success(request, f'Деталь "{part.name}" добавлена в расчет')
        else:
            messages.success(request, f'Услуга для детали "{part.name}" обновлена')
            
        return redirect('calculator:calculator', car_model_slug=part.projection.car_model.slug)
            
    except BodyPart.DoesNotExist:
        messages.error(request, 'Деталь не найдена')
    except Exception as e:
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