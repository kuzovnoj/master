from django.contrib import admin
from .models import Auto, ZakazNaryad, Client, Oplata
# Register your models here.
from django.db import models
from django.db.models import Count, Sum, Avg, Max, Min

@admin.register(Auto)
class AutoAdmin(admin.ModelAdmin):
    list_display = ('id', 'marka', 'gos_num', 'time_create')
    list_editable = ('marka', 'gos_num')
    list_per_page = 12


@admin.register(ZakazNaryad)
class ZakazNaryadAdmin(admin.ModelAdmin):
    list_display = ('id', 'auto', 'master', 'client', 'remont', 'price',
                    'avans', 'raskhod', 'time_create', 'time_update', 'oplata')
    list_editable = ('master', 'remont', 'price', 'avans',
                     'raskhod')
    list_per_page = 12

    def oplata(self, zakaznaryad: ZakazNaryad):
        z1 = ZakazNaryad.objects.filter(oplata__zakaz=zakaznaryad.id).aggregate(Sum('oplata__amount'))
        return z1['oplata__amount__sum']

@admin.register(Client)
class AutoAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone')
    list_editable = ('name', 'phone')
    list_per_page = 12

@admin.register(Oplata)
class OplataAdmin(admin.ModelAdmin):
    list_display = ('id', 'zakaz', 'amount', 'time_create')
    list_editable = ('zakaz', 'amount')
    list_per_page = 12