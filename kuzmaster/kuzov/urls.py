from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
        path('', views.KuzovHome.as_view(), name='home'),  # http://127.0.0.1:8000
        path('addauto/', views.AddAuto.as_view(), name='auto'),
        path('zakaz_naryad/', views.ZakazAddAuto.as_view(), name='zakaz_naryad'),
        path('zakaz_naryad2/', views.ZakazNaryad2.as_view(), name='zakaz_naryad2'),
        path('get_avans/', views.AddAvans.as_view(), name='get_avans'),
        path('raskhod/', views.AddRaskhod.as_view(), name='raskhod'),
        path('client/', views.AddClient.as_view(), name='client'),
        path('oplata/', views.AddOplata.as_view(), name='oplata'),
]
