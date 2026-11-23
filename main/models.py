from django.db import models

from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Название категории')

    def __str__(self):
        return self.name


class DesignRequest(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новая'),
        ('in_progress', 'Принято в работу'),
        ('completed', 'Выполнено'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name='Категория'
    )

    name = models.CharField(
        max_length=200,
        verbose_name='Название заявки'
    )

    description = models.TextField(
        verbose_name='Описание'
    )

    image = models.ImageField(
        upload_to='requests/',
        verbose_name='Изображение помещения'
    )

    design_image = models.ImageField(
        upload_to='designs/',
        blank=True,
        null=True,
        verbose_name='Готовый дизайн'
    )

    admin_comment = models.TextField(
        blank=True,
        verbose_name='Комментарий администратора'
    )

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default='Новая',
        verbose_name='Статус'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'

    def __str__(self):
        return self.name
