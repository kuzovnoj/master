from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal

class WorkCategory(models.Model):
    """Категория работ (покраска, жестяные работы и т.д.)"""
    name = models.CharField('Название категории', max_length=100)
    slug = models.SlugField('URL', max_length=100, unique=True)
    description = models.TextField('Описание', blank=True)
    background_image = models.ImageField(
        'Фоновое изображение',
        upload_to='works/categories/',
        help_text='Изображение, которое будет фоном при выборе категории'
    )
    icon = models.CharField(
        'Иконка Font Awesome',
        max_length=50,
        help_text='Например: fa-paint-roller, fa-wrench, fa-car',
        default='fa-wrench'
    )
    order = models.PositiveIntegerField('Порядок', default=0)
    is_active = models.BooleanField('Активно', default=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    
    class Meta:
        verbose_name = 'Категория работ'
        verbose_name_plural = 'Категории работ'
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name

class BodyPart(models.Model):
    """Деталь кузова для прайса"""
    name = models.CharField('Название детали', max_length=100)
    slug = models.SlugField('URL', max_length=100)
    order = models.PositiveIntegerField('Порядок', default=0)
    is_active = models.BooleanField('Активно', default=True)
    
    class Meta:
        verbose_name = 'Деталь кузова'
        verbose_name_plural = 'Детали кузова'
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name

class PriceItem(models.Model):
    """Позиция прайс-листа"""
    category = models.ForeignKey(
        WorkCategory,
        on_delete=models.CASCADE,
        verbose_name='Категория',
        related_name='price_items'
    )
    part = models.ForeignKey(
        BodyPart,
        on_delete=models.CASCADE,
        verbose_name='Деталь',
        related_name='price_items'
    )
    price_from = models.DecimalField(
        'Цена от',
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    description = models.CharField(
        'Краткое описание',
        max_length=200,
        blank=True,
        help_text='Например: "с подготовкой" или "под ключ"'
    )
    order = models.PositiveIntegerField('Порядок', default=0)
    is_active = models.BooleanField('Активно', default=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)
    
    class Meta:
        verbose_name = 'Позиция прайса'
        verbose_name_plural = 'Позиции прайса'
        ordering = ['category', 'order', 'part']
        unique_together = ['category', 'part']  # Одна цена на категорию+деталь
    
    def __str__(self):
        return f"{self.category.name} - {self.part.name}: от {self.price_from} руб."