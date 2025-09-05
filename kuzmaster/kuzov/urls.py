from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
        path('', views.KuzovHome.as_view(), name='home'),
        path('done/', views.KuzovHomeDone.as_view(), name='home_done'),
        path('zakaz_naryad/', views.add_auto_view, name='zakaz_naryad'),
        path('zakaz_naryad2/<slug:pk_slug>/', views.ZakazNaryad2.as_view(), name='zakaz_naryad2'),
        path('get_avans/', views.AddAvans.as_view(), name='get_avans'),
        path('raskhod/', views.AddRaskhod.as_view(), name='raskhod'),
        path('client/<slug:pk_auto>/', views.addclient_view, name='client'),
        path('oplata/', views.AddOplata.as_view(), name='oplata'),
        path('order/<slug:order_id>/', views.ShowOrder.as_view(), name='show_order'),
        path('edit-order/<int:pk>/', views.EditOrder.as_view(), name='edit_order'),
        path('edit-auto/<int:pk>/', views.EditAuto.as_view(), name='edit_auto'),
        path('edit-raskhod/<int:pk>/', views.EditRaskhod.as_view(), name='edit_raskhod'),
        path('order_raskhod/<slug:order_id>/', views.OrderRaskhod.as_view(), name='order_raskhod'),
        path('order_spareparts/<slug:order_id>/', views.OrderSparePart.as_view(), name='order_spareparts'),
        path('order_avans/<slug:order_id>/', views.OrderAvans.as_view(), name='order_avans'),
        path('order_oplata/<slug:order_id>/', views.OrderOplata.as_view(), name='order_oplata'),
        path('api/', views.APIKuzovView.as_view({'get': 'list'}), name='api_home'),
]

