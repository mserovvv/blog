from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import Comment


@receiver(post_save, sender=Comment)
def update_comment_count_on_save(sender, instance, **kwargs):
    """
    Обновляет количество комментариев при
    добавлении или изменении комментария.
    """
    instance.post.update_comment_count()


@receiver(post_delete, sender=Comment)
def update_comment_count_on_delete(sender, instance, **kwargs):
    """Обновляет количество комментариев при удалении комментария."""
    instance.post.update_comment_count()
