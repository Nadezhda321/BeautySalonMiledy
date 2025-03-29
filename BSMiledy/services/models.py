from django.db import models

class TypeService(models.Model):
    name = models.CharField('Наименование вида услуг', max_length=100)
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Вид услуги'
        verbose_name_plural = 'Виды услуг'

class Service(models.Model):
    PRICE_TYPE_CHOICES = [
        ('fixed', 'Фиксированная цена'),
        ('flexible', 'Гибкая цена'),
    ]

    name = models.CharField('Наименование', max_length=100, default='Новая услуга')
    # description = models.CharField('Описание', max_length=250)
    description = models.TextField('Описание', max_length=750, null=True)
    photo = models.ImageField('Фото', null=True, upload_to='services/')

    type_service = models.ForeignKey(TypeService, on_delete=models.CASCADE, related_name='services', verbose_name='Вид услуги')

    min_price = models.IntegerField('Минимальная стоимость')
    type_price = models.CharField('Тип цены', max_length=50, choices=PRICE_TYPE_CHOICES)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'


class PhotoService(models.Model):
    date_add = models.DateField('Дата добавления')
    photo = models.ImageField('Фото', upload_to='gallery/')
    type_service = models.ForeignKey(TypeService, on_delete=models.CASCADE, related_name='gallery_images', verbose_name='Вид услуги')
    
    #Какая информация будет выводиться когда мы выводим сам по себе объект
    def __str__(self):
        return f"Фото для {self.type_service.name} ({self.date_add})"

    class Meta:
        verbose_name = 'Фотогалерея'
        verbose_name_plural = 'Фотогалерея'
    