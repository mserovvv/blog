from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils.text import Truncator
from django.utils.timezone import now

from core.models import PublishedModel
from .constants import HELP_CATEGORY, HELP_POST, MAX_LEN

User = get_user_model()


class Category(PublishedModel):
    """
    Модель для категорий постов.
    """
    title = models.CharField(max_length=256, verbose_name="Заголовок")
    description = models.TextField(verbose_name="Описание")
    slug = models.SlugField(
        unique=True,
        help_text=f"Идентификатор страницы для URL; разрешены {HELP_CATEGORY}",
        verbose_name="Идентификатор",
    )

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return Truncator(self.title).words(MAX_LEN)


class Location(PublishedModel):
    """
    Модель для местоположений.
    """
    name = models.CharField(max_length=256, verbose_name="Название места")

    class Meta:
        verbose_name = "местоположение"
        verbose_name_plural = "Местоположения"

    def __str__(self):
        return Truncator(self.name).words(MAX_LEN)


class Post(PublishedModel):
    """
    Модель для публикаций в блоге.
    """
    title = models.CharField(max_length=256, verbose_name="Заголовок")
    text = models.TextField(verbose_name="Текст")
    pub_date = models.DateTimeField(
        help_text=f"Если установить дату и время в будущем — {HELP_POST}",
        verbose_name="Дата и время публикации",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Автор публикации",
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Местоположение",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Категория",
    )
    image = models.ImageField("Фото", blank=True, null=True)
    comment_count = models.IntegerField(default=0)
    is_published = models.BooleanField(
        default=True,
        verbose_name="Разрешение на публикацию",
    )
    is_scheduled = models.BooleanField(
        default=False,
        verbose_name="Запланирован",
    )

    def save(self, *args, **kwargs):
        """
        Переопределяет сохранение для обновления поля is_scheduled.
        """
        if self.is_published and self.pub_date <= now():
            self.is_scheduled = True
        else:
            self.is_scheduled = False
        super().save(*args, **kwargs)

    def update_comment_count(self):
        """
        Обновляет количество комментариев для поста.
        """
        self.comment_count = self.comments.count()
        self.save(update_fields=["comment_count"])

    def get_absolute_url(self):
        """
        Возвращает URL для просмотра деталей поста.
        """
        return reverse("blog:post_detail", kwargs={"pk": self.pk})

    class Meta:
        verbose_name = "публикация"
        verbose_name_plural = "Публикации"
        default_related_name = "posts"
        ordering = ["-pub_date"]

    def __str__(self):
        return Truncator(self.title).words(MAX_LEN)


class Comment(models.Model):
    """
    Модель для комментариев к постам.
    """
    text = models.TextField("Текст комментария")
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="comments",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Автор",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания",
    )

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
        ordering = ("created_at",)
