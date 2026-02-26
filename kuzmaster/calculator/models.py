from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal

class CarModel(models.Model):
    """Модель автомобиля (тип кузова)"""
    name = models.CharField('Название', max_length=100)
    slug = models.SlugField('URL-идентификатор', unique=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    
    class Meta:
        verbose_name = 'Модель автомобиля'
        verbose_name_plural = 'Модели автомобилей'
        ordering = ['name']
    
    def __str__(self):
        return self.name

class Projection(models.Model):
    """Проекция (ракурс) автомобиля"""
    PROJECTION_TYPES = [
        ('front_left', 'Спереди слева'),
        ('rear_right', 'Сзади справа'),
    ]
    
    car_model = models.ForeignKey(
        CarModel, 
        on_delete=models.CASCADE,
        verbose_name='Модель автомобиля',
        related_name='projections'
    )
    name = models.CharField('Название', max_length=100)
    code = models.CharField('Код проекции', max_length=20, choices=PROJECTION_TYPES)
    image = models.ImageField('Изображение', upload_to='calculator/projections/')
    order = models.PositiveIntegerField('Порядок', default=0)
    
    class Meta:
        verbose_name = 'Проекция'
        verbose_name_plural = 'Проекции'
        ordering = ['order']
        unique_together = ['car_model', 'code']  # Одна проекция одного типа для модели
    
    def __str__(self):
        return f"{self.car_model.name} - {self.name}"

class Service(models.Model):
    """Услуга (вид работы)"""
    name = models.CharField('Название услуги', max_length=100)
    price = models.DecimalField(
        'Базовая стоимость', 
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    color = models.CharField(
        'Цвет заливки', 
        max_length=50, 
        default='rgba(40, 167, 69, 0.2)',
        help_text='Формат: rgba(255, 0, 0, 0.3) или #RRGGBB'
    )
    description = models.TextField('Описание', blank=True)
    is_active = models.BooleanField('Активна', default=True)
    order = models.PositiveIntegerField('Порядок', default=0)
    
    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'
        ordering = ['order']
    
    def __str__(self):
        return f"{self.name} - {self.price} руб."

class BodyPart(models.Model):
    """Деталь кузова"""
    projection = models.ForeignKey(
        Projection,
        on_delete=models.CASCADE,
        verbose_name='Проекция',
        related_name='parts'
    )
    name = models.CharField('Название детали', max_length=100)
    coordinates = models.TextField(
        'Координаты контура',
        help_text='SVG path или координаты полигона (например: "M10,10 L20,20 L30,10 Z")'
    )
    order = models.PositiveIntegerField('Порядок отображения', default=0)
    is_active = models.BooleanField('Активна', default=True)
    
    class Meta:
        verbose_name = 'Деталь кузова'
        verbose_name_plural = 'Детали кузова'
        ordering = ['projection', 'order']
    
    def __str__(self):
        return f"{self.projection.car_model.name} - {self.projection.name} - {self.name}"

class CalculationSession(models.Model):
    """Сессия расчета пользователя"""
    session_key = models.CharField('Ключ сессии', max_length=255, db_index=True)
    car_model = models.ForeignKey(
        CarModel,
        on_delete=models.CASCADE,
        verbose_name='Модель автомобиля'
    )
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)
    
    class Meta:
        verbose_name = 'Сессия расчета'
        verbose_name_plural = 'Сессии расчетов'
    
    def __str__(self):
        return f"Сессия {self.session_key[:10]}... от {self.created_at}"
    
    def get_total_price(self):
        """Получить общую сумму всех выбранных деталей"""
        total = self.selected_parts.aggregate(
            total=models.Sum('price')
        )['total'] or Decimal('0')
        return total

class SelectedPart(models.Model):
    """Выбранная пользователем деталь с услугой"""
    session = models.ForeignKey(
        CalculationSession,
        on_delete=models.CASCADE,
        verbose_name='Сессия',
        related_name='selected_parts'
    )
    part = models.ForeignKey(
        BodyPart,
        on_delete=models.CASCADE,
        verbose_name='Деталь'
    )
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        verbose_name='Услуга'
    )
    price = models.DecimalField(
        'Стоимость',
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    created_at = models.DateTimeField('Дата добавления', auto_now_add=True)
    
    class Meta:
        verbose_name = 'Выбранная деталь'
        verbose_name_plural = 'Выбранные детали'
        ordering = ['-created_at']
        # Одна деталь может быть выбрана только один раз в сессии
        unique_together = ['session', 'part']
    
    def __str__(self):
        return f"{self.part.name} - {self.service.name} - {self.price} руб."
    
    def save(self, *args, **kwargs):
        # Автоматически устанавливаем цену из услуги
        if not self.price:
            self.price = self.service.price
        super().save(*args, **kwargs)


class PartService(models.Model):
    """Связь детали с услугой и специфическая цена"""
    part = models.ForeignKey(
        BodyPart,
        on_delete=models.CASCADE,
        verbose_name='Деталь',
        related_name='part_services'
    )
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        verbose_name='Услуга',
        related_name='part_services'
    )
    price = models.DecimalField(
        'Стоимость',
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    is_active = models.BooleanField('Активно', default=True)
    
    class Meta:
        verbose_name = 'Услуга для детали'
        verbose_name_plural = 'Услуги для деталей'
        unique_together = ['part', 'service']  # Одна комбинация деталь-услуга
        ordering = ['part', 'service']
    
    def __str__(self):
        return f"{self.part.name} - {self.service.name}: {self.price} руб."

class Appointment(models.Model):
    """Запись на осмотр"""
    TIME_SLOTS = [
        ('10:00-12:00', '10:00 - 12:00'),
        ('12:00-14:00', '12:00 - 14:00'),
        ('14:00-16:00', '14:00 - 16:00'),
        ('16:00-18:00', '16:00 - 18:00'),
        ('18:00-20:00', '18:00 - 20:00'),
    ]
    
    date = models.DateField('Дата записи')
    time_slot = models.CharField('Временной слот', max_length=20, choices=TIME_SLOTS)
    name = models.CharField('Имя', max_length=100)
    phone = models.CharField('Телефон', max_length=20)
    car_model = models.CharField('Марка авто', max_length=100, blank=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    is_processed = models.BooleanField('Обработано', default=False)
    
    class Meta:
        verbose_name = 'Запись на осмотр'
        verbose_name_plural = 'Записи на осмотр'
        ordering = ['-date', 'time_slot']
    
    def __str__(self):
        return f"{self.name} - {self.date} {self.time_slot}"

class CallbackRequest(models.Model):
    """Заказ звонка"""
    name = models.CharField('Имя', max_length=100)
    phone = models.CharField('Телефон', max_length=20)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    is_processed = models.BooleanField('Обработано', default=False)
    
    class Meta:
        verbose_name = 'Заказ звонка'
        verbose_name_plural = 'Заказы звонков'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.phone}"