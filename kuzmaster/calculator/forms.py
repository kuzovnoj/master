from django import forms
from .models import Appointment, CallbackRequest
from django.core.validators import RegexValidator

class AppointmentForm(forms.ModelForm):
    phone = forms.CharField(
        label='Телефон',
        validators=[RegexValidator(regex=r'^\+?7?\d{10,15}$', message='Введите корректный номер телефона')],
        widget=forms.TextInput(attrs={'placeholder': '+7 (999) 123-45-67', 'class': 'form-control'})
    )
    
    class Meta:
        model = Appointment
        fields = ['date', 'time_slot', 'name', 'phone', 'car_model']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'time_slot': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'placeholder': 'Ваше имя', 'class': 'form-control'}),
            'car_model': forms.TextInput(attrs={'placeholder': 'Марка и модель авто', 'class': 'form-control'}),
        }

class CallbackForm(forms.ModelForm):
    phone = forms.CharField(
        label='Телефон',
        validators=[RegexValidator(regex=r'^\+?7?\d{10,15}$', message='Введите корректный номер телефона')],
        widget=forms.TextInput(attrs={'placeholder': '+7 (999) 123-45-67', 'class': 'form-control'})
    )
    
    class Meta:
        model = CallbackRequest
        fields = ['name', 'phone']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Ваше имя', 'class': 'form-control'}),
        }