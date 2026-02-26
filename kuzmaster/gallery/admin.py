from django.contrib import admin
from django.utils.html import format_html
from .models import CarBrand, CarModel, GalleryImage

class CarModelInline(admin.TabularInline):
    model = CarModel
    extra = 1
    prepopulated_fields = {'slug': ('name',)}
    fields = ['name', 'slug', 'order']

@admin.register(CarBrand)
class CarBrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'order', 'models_count', 'created_at']
    list_editable = ['order']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']
    inlines = [CarModelInline]
    
    def models_count(self, obj):
        return obj.models.count()
    models_count.short_description = 'Количество моделей'

@admin.register(CarModel)
class CarModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'brand', 'order', 'images_count']
    list_filter = ['brand']
    list_editable = ['order']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'brand__name']
    
    def images_count(self, obj):
        return obj.images.count()
    images_count.short_description = 'Фотографий'

@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ['car_model', 'description', 'order', 'is_active', 'created_at', 'preview']
    list_filter = ['car_model__brand', 'car_model', 'is_active']
    list_editable = ['order', 'is_active']
    search_fields = ['car_model__brand__name', 'car_model__name', 'description']
    raw_id_fields = ['car_model']
    fieldsets = (
        ('Модель автомобиля', {
            'fields': ('car_model',)
        }),
        ('Фотографии', {
            'fields': ('before_image', 'after_image', 'description')
        }),
        ('Настройки', {
            'fields': ('order', 'is_active')
        }),
    )
    
    def preview(self, obj):
        if obj.before_image and obj.after_image:
            return format_html(
                '<div style="display: flex; gap: 5px;">'
                '<img src="{}" width="50" height="50" style="object-fit: cover;">'
                '<img src="{}" width="50" height="50" style="object-fit: cover;">'
                '</div>',
                obj.before_image.url, obj.after_image.url
            )
        return "-"
    preview.short_description = 'Превью'