from django.urls import path
from . import views

app_name = 'calculator'

urlpatterns = [
    path('<slug:car_model_slug>/', views.calculator_view, name='calculator'),
    path('part/add/', views.add_part_view, name='add_part'),
    path('part/remove/<int:selected_part_id>/', views.remove_part_view, name='remove_part'),
    path('part/update/<int:selected_part_id>/', views.update_service_view, name='update_service'),
    path('api/create-appointment/', views.create_appointment, name='create_appointment'),
    path('api/create-callback/', views.create_callback, name='create_callback'),
]