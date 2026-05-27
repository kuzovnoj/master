from django.db import models
from django.core.validators import MinLengthValidator
from kuzmaster.image_utils import compress_image

class CarBrand(models.Model):
    """Марка автомобиля"""
    name = models.CharField('Марка', max_length=100, unique=True)
    slug = models.SlugField('URL', max_length=100, unique=True)
    order = models.PositiveIntegerField('Порядок', default=0)
    created_at = models.DateTimeField('Дата добавления', auto_now_add=True)
    
    class Meta:
        verbose_name = 'Марка автомобиля'
        verbose_name_plural = 'Марки автомобилей'
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name

class CarModel(models.Model):
    """Модель автомобиля"""
    brand = models.ForeignKey(
        CarBrand, 
        on_delete=models.CASCADE, 
        verbose_name='Марка',
        related_name='models'
    )
    name = models.CharField('Модель', max_length=100)
    slug = models.SlugField('URL', max_length=100)
    order = models.PositiveIntegerField('Порядок', default=0)
    created_at = models.DateTimeField('Дата добавления', auto_now_add=True)
    
    class Meta:
        verbose_name = 'Модель автомобиля'
        verbose_name_plural = 'Модели автомобилей'
        ordering = ['brand', 'order', 'name']
        unique_together = ['brand', 'name']  # Одна марка не может иметь две одинаковые модели
    
    def __str__(self):
        return f"{self.brand.name} {self.name}"

class GalleryImage(models.Model):
    """Фотография работы до/после"""
    car_model = models.ForeignKey(
        CarModel,
        on_delete=models.CASCADE,
        verbose_name='Модель авто',
        related_name='images'
    )
    
    # Фотографии
    before_image = models.ImageField(
        'Фото ДО',
        upload_to='gallery/before/%Y/%m/',
        help_text='Фотография до ремонта'
    )
    after_image = models.ImageField(
        'Фото ПОСЛЕ',
        upload_to='gallery/after/%Y/%m/',
        help_text='Фотография после ремонта'
    )
    
    # Дополнительная информация
    description = models.CharField(
        'Описание работы',
        max_length=200,
        blank=True,
        help_text='Например: Замена крыла и покраска'
    )
    
    # Сортировка и статус
    order = models.PositiveIntegerField('Порядок отображения', default=0)
    is_active = models.BooleanField('Активно', default=True)
    created_at = models.DateTimeField('Дата добавления', auto_now_add=True)
    
    class Meta:
        verbose_name = 'Фотография работы'
        verbose_name_plural = 'Фотографии работ'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.car_model} - {self.created_at.strftime('%d.%m.%Y')}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.before_image:
            compress_image(self.before_image, max_width=1920, max_height=1920, quality=85)
        if self.after_image:
            compress_image(self.after_image, max_width=1920, max_height=1920, quality=85)

    @property
    def car_brand(self):
        return self.car_model.brand