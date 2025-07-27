from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
        path('', views.KuzovHome.as_view(), name='home'),  # http://127.0.0.1:8000
        path('zakaz_naryad/', views.add_auto_view, name='zakaz_naryad'),
        path('zakaz_naryad2/<slug:pk_slug>/', views.ZakazNaryad2.as_view(), name='zakaz_naryad2'),
        path('get_avans/', views.AddAvans.as_view(), name='get_avans'),
        path('raskhod/', views.AddRaskhod.as_view(), name='raskhod'),
        path('client/<slug:pk_auto>/', views.addclient_view, name='client'),
        path('oplata/', views.AddOplata.as_view(), name='oplata'),
        path('order/<slug:order_id>/', views.ShowOrder.as_view(), name='show_order'),
        path('edit-order/<int:pk>/', views.EditOrder.as_view(), name='edit_order'),
]

