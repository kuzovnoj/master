from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
        path('', views.KuzovHome.as_view(), name='home'),  # http://127.0.0.1:8000
        path('addauto/', views.AddAuto.as_view(), name='auto'),
        path('zakaz_naryad/', views.zakaz, name='zakaz_naryad'),
        path('get_avans/', views.avans, name='get_avans'),
        path('raskhod/', views.raskhod, name='raskhod'),
]
