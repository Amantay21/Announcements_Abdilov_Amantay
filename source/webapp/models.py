from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import MinLengthValidator

STATUS_CHOICES = (
    ('moderation', 'На модерацию'),
    ('published', 'Опубликовано'),
    ('rejected', 'Отклонено'),
    ('pending_deletion', 'На удаление'),
)


class Category(models.Model):
    title = models.CharField(max_length=200, null=False, blank=False, verbose_name='Название')

    def __str__(self):
        return f'{self.id}. {self.title}'


class AbstractModel(models.Model):
    created = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    published_at = models.DateTimeField(blank=True, null=True, verbose_name='Время публикации')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Время изменения')

    class Meta:
        abstract = True


class Announcements(AbstractModel):
    image = models.CharField(max_length=5000, null=True, blank=True, verbose_name='Фотография')
    title = models.CharField(max_length=250, null=False, blank=False, validators=[MinLengthValidator(4), ],
                             verbose_name="Заголовок")
    description = models.TextField(max_length=3000, null=False, blank=False, verbose_name='Контент')
    author = models.ForeignKey(get_user_model(), default=1, related_name='announcements', on_delete=models.CASCADE,
                               verbose_name="Автор")
    category = models.ForeignKey('webapp.Category',
                                 on_delete=models.RESTRICT,
                                 verbose_name='Категория',
                                 related_name='categories',
                                 null=True)
    amount = models.DecimalField(max_digits=7, decimal_places=2, null=False, blank=False, verbose_name="Цена")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='moderation', verbose_name='Статус')

    def __str__(self):
        return f'{self.id}. {self.title}'


class Comment(AbstractModel):
    announcements = models.ForeignKey('webapp.Announcements', related_name='comments', on_delete=models.CASCADE,
                                      verbose_name='Обьявление')
    text = models.TextField(max_length=400, verbose_name='Комментарий')
    author = models.ForeignKey(get_user_model(), related_name='comments', on_delete=models.CASCADE)

    def __str__(self):
        return self.text[:20]
