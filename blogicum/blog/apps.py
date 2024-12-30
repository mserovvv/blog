from django.apps import AppConfig

class BlogConfig(AppConfig):
    """
    Конфигурация приложения "blog".
    """
    default_auto_field = "django.db.models.BigAutoField"  # Тип поля ID по умолчанию для моделей.
    name = "blog"  # Имя приложения.
    verbose_name = "Блог"  # Название для админки.

    def ready(self):
        """
        Инициализация приложения (например, подключение сигналов).
        """
        import blog.signals  # Импорт сигналов приложения.
