from django.db import models
from django.conf import settings
from users.models import NULLABLE


class Blog(models.Model):
    title = models.CharField(max_length=100, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Содержимое статьи')
    picture = models.ImageField(upload_to='blog/', verbose_name='Изображение', **NULLABLE)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    views_count = models.IntegerField(default=0, verbose_name='Кол-во просмотров')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Публикатор')
    is_published = models.BooleanField(default=False, verbose_name='Опубликовано')

    def __str__(self):
        return f'{self.title}, {self.user}, {self.created_at}, {self.is_published}'

    class Meta:
        verbose_name = 'блог'
        verbose_name_plural = 'блоги'
