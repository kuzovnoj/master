from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
        path('', views.KuzovHome.as_view(), name='home'),  # http://127.0.0.1:8000
        path('addauto/', views.AddAuto.as_view(), name='auto')
]
