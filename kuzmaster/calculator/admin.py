from django.contrib import admin
from django.utils.html import format_html
from .models import CarModel, Projection, Service, BodyPart, CalculationSession, SelectedPart

@admin.register(CarModel)
class CarModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_at']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']

@admin.register(Projection)
class ProjectionAdmin(admin.ModelAdmin):
    list_display = ['name', 'car_model', 'code', 'order', 'image_preview']
    list_filter = ['car_model', 'code']
    search_fields = ['name', 'car_model__name']
    raw_id_fields = ['car_model']
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" height="auto" />', obj.image.url)
        return "Нет изображения"
    image_preview.short_description = 'Превью'

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'is_active', 'order']
    list_editable = ['price', 'is_active', 'order']
    list_filter = ['is_active']
    search_fields = ['name', 'description']

@admin.register(BodyPart)
class BodyPartAdmin(admin.ModelAdmin):
    list_display = ['name', 'projection', 'order', 'is_active', 'coordinates_preview']
    list_filter = ['projection__car_model', 'projection', 'is_active']
    search_fields = ['name']
    raw_id_fields = ['projection']
    fieldsets = (
        ('Основная информация', {
            'fields': ('projection', 'name', 'order', 'is_active')
        }),
        ('Координаты', {
            'fields': ('coordinates',),
            'description': 'Введите координаты для отрисовки контура на изображении'
        }),
    )
    
    def coordinates_preview(self, obj):
        if obj.coordinates:
            return format_html('<code>{}</code>', obj.coordinates[:50] + '...')
        return "-"
    coordinates_preview.short_description = 'Координаты'

@admin.register(CalculationSession)
class CalculationSessionAdmin(admin.ModelAdmin):
    list_display = ['id', 'session_key', 'car_model', 'created_at', 'updated_at', 'total_price']
    list_filter = ['car_model', 'created_at']
    search_fields = ['session_key']
    readonly_fields = ['session_key', 'created_at', 'updated_at']
    
    def total_price(self, obj):
        return obj.get_total_price()
    total_price.short_description = 'Общая сумма'

@admin.register(SelectedPart)
class SelectedPartAdmin(admin.ModelAdmin):
    list_display = ['part', 'service', 'price', 'session', 'created_at']
    list_filter = ['service', 'created_at']
    search_fields = ['part__name', 'session__session_key']
    raw_id_fields = ['session', 'part', 'service']