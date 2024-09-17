from django.db import models
from users.models import NULLABLE, User


class ClientService(models.Model):
    """Модель Клиент сервера"""
    email = models.EmailField(unique=True, verbose_name='почта')
    surname_name_patronymic = models.CharField(max_length=100, verbose_name='Ф.И.О.', **NULLABLE)
    comment = models.CharField(max_length=100, verbose_name='Комментарий')
    company = models.ForeignKey(User, on_delete=models.CASCADE, max_length=50, verbose_name='Название компании')

    def __str__(self):
        return f'{self.email}'

    class Meta:
        verbose_name = 'Клиент сервера'
        verbose_name_plural = 'Клиенты сервера'


class Blasts(models.Model):
    """Модель Рассылка"""
    FREQUENCY_CHOICES = [
        ('ежедневный', 'Один раз в день'),
        ('еженедельно', 'Раз в неделю'),
        ('ежемесячно', 'Раз в месяц'),
    ]

    STATUS_CHOICES = [
        ('созданный', 'Созданный'),
        ('запущенный', 'Запущенный'),
        ('завершенный', 'Завершенный'),
    ]
    start_datetime = models.DateTimeField(verbose_name='Дата и время начала')
    end_datetime = models.DateTimeField(verbose_name='Дата и время окончания')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время первой отправки рассылки')
    frequency = models.CharField(max_length=50, choices=FREQUENCY_CHOICES, verbose_name='Периодичность')
    status = models.CharField(choices=STATUS_CHOICES, default='Созданный', verbose_name='Статус рассылки')
    company = models.ForeignKey(User, on_delete=models.CASCADE, max_length=50, verbose_name='Название компании')
    email = models.ManyToManyField(ClientService, verbose_name='Почта клиента')
    title = models.CharField(max_length=100, verbose_name='Тема Рассылки')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'


class Message(models.Model):
    """Модель сообщения"""
    title = models.ForeignKey(Blasts, on_delete=models.CASCADE, verbose_name='Тема письма')
    body = models.TextField(verbose_name='Тело письма')
    user = models.CharField(verbose_name='Автор письма')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'


class DeliveryAttempt(models.Model):
    """Модель Попытка рассылки"""
    ATTEMPT_STATUS_CHOICES = [
        ('успешно отправлено', 'Успешный'),
        ('ошибка', 'Неудачный'),
    ]
    attempt_datetime = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время последней попытки')
    attempt_status = models.CharField(max_length=50, choices=ATTEMPT_STATUS_CHOICES, verbose_name='Статус попытки')
    mail_server_response = models.TextField(**NULLABLE, verbose_name='Ответ почтового сервера')
    title = models.ForeignKey(Blasts, on_delete=models.CASCADE, verbose_name='Тема Рассылки')

    def __str__(self):
        return f'Попытка - {self.attempt_datetime}'

    class Meta:
        verbose_name = 'Попытка рассылки'
        verbose_name_plural = 'Попытки рассылок'
