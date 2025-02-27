from django.contrib import admin
from .models import Auto, ZakazNaryad, Client
# Register your models here.


@admin.register(Auto)
class AutoAdmin(admin.ModelAdmin):
    list_display = ('id', 'marka', 'gos_num', 'time_create')
    list_editable = ('marka', 'gos_num')
    list_per_page = 12


@admin.register(ZakazNaryad)
class AutoAdmin(admin.ModelAdmin):
    list_display = ('id', 'auto', 'master', 'client', 'remont', 'price',
                    'predoplata', 'avans', 'raskhod', 'time_create', 'time_update')
    list_editable = ('master', 'remont', 'price', 'predoplata', 'avans',
                     'raskhod')
    list_per_page = 12

@admin.register(Client)
class AutoAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone')
    list_editable = ('name', 'phone')
    list_per_page = 12