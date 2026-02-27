from django.contrib import admin
from django.utils.html import format_html
from .models import WorkCategory, BodyPart, PriceItem

class PriceItemInline(admin.TabularInline):
    model = PriceItem
    extra = 1
    fields = ['part', 'price_from', 'description', 'order', 'is_active']
    autocomplete_fields = ['part']

@admin.register(WorkCategory)
class WorkCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'order', 'icon', 'is_active', 'items_count', 'preview']
    list_editable = ['order', 'is_active']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'description']
    inlines = [PriceItemInline]
    
    def items_count(self, obj):
        return obj.price_items.count()
    items_count.short_description = 'Позиций'
    
    def preview(self, obj):
        if obj.background_image:
            return format_html(
                '<img src="{}" width="50" height="50" style="object-fit: cover; border-radius: 5px;">',
                obj.background_image.url
            )
        return "-"
    preview.short_description = 'Фон'

@admin.register(BodyPart)
class BodyPartAdmin(admin.ModelAdmin):
    list_display = ['name', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']

@admin.register(PriceItem)
class PriceItemAdmin(admin.ModelAdmin):
    list_display = ['category', 'part', 'price_from', 'description', 'order', 'is_active']
    list_editable = ['price_from', 'order', 'is_active']
    list_filter = ['category', 'part', 'is_active']
    search_fields = ['category__name', 'part__name', 'description']
    autocomplete_fields = ['category', 'part']