from django.db import models
from users.models import NULLABLE, User


# Create your models here.
class ClientService(models.Model):
    """Модель Клиент сервера"""
    email = models.EmailField(unique=True, verbose_name='почта')
    surname_name_patronymic = models.CharField(max_length=100, verbose_name='Ф.И.О.', **NULLABLE)
    comment = models.CharField(max_length=100, verbose_name='Комментарий')
    company = models.ForeignKey(User.company, on_delete=models.CASCADE, max_length=50, verbose_name='Название компании')

    def __str__(self):
        return f'{self.email}, {self.surname_name_patronymic}, {self.comment}, {self.company}'

    class Meta:
        verbose_name = 'Клиент сервера'
        verbose_name_plural = 'Клиенты сервера'


class Blasts(models.Model):
    """Модель Рассылка"""
    FREQUENCY_CHOICES = [
        ('daily', 'Once a day'),
        ('weekly', 'Once a week'),
        ('monthly', 'Once a month'),
    ]

    STATUS_CHOICES = [
        ('created', 'Created'),
        ('launched', 'Launched'),
        ('completed', 'Completed'),
    ]

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время первой отправки рассылки')
    frequency = models.CharField(max_length=10, choices=FREQUENCY_CHOICES, verbose_name='Периодичность')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, verbose_name='статус рассылки')
    company = models.ForeignKey(User.company, on_delete=models.CASCADE, max_length=50, verbose_name='Название компании')
    email = models.ForeignKey(ClientService.email, on_delete=models.CASCADE, verbose_name='Почта клиента')
    title = models.CharField(max_length=100, verbose_name='Тема Рассылки')

    def __str__(self):
        return f'{self.created_at}, {self.frequency}, {self.status}'

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'


class Message(models.Model):
    """Модель сообщения"""
    title = models.ForeignKey(Blasts.title, on_delete=models.CASCADE, verbose_name='Тема письма')
    body = models.TextField(verbose_name='Тело письма')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'


class DeliveryAttempt(models.Model):
    """Модель Попытка рассылки"""
    ATTEMPT_STATUS_CHOICES = [
        ('success', 'Successful'),
        ('failure', 'Unsuccessful'),
    ]
    attempt_datetime = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время последней попытки')
    attempt_status = models.CharField(max_length=10, choices=ATTEMPT_STATUS_CHOICES, verbose_name='Статус попытки')
    mail_server_response = models.TextField(**NULLABLE, verbose_name='Ответ почтового сервера')
    email = models.ForeignKey(ClientService, on_delete=models.CASCADE, verbose_name='Почта')
    title = models.ForeignKey(Blasts.title, on_delete=models.CASCADE, verbose_name='Тема Рассылки')

    def __str__(self):
        return f'Попытка - {self.attempt_datetime}'

    class Meta:
        verbose_name = 'Попытка рассылки'
        verbose_name_plural = 'Попытки рассылок'
