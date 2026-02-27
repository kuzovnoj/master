from django.urls import path
from . import views

app_name = 'works'

urlpatterns = [
    path('', views.price_list_view, name='price_list'),
]