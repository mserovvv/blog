from django.contrib import admin

from .models import Category, Comment, Location, Post

# Указываем значение, которое будет отображаться в админке, если поле не задано
admin.site.empty_value_display = "Не задано"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Админ-класс для управления объектами модели Category.
    """
    list_display = ("title", "description", "is_published")  # Поля, отображаемые в списке
    list_editable = ("is_published",)  # Поля, доступные для редактирования в списке
    search_fields = ("title", "description")  # Поля, по которым выполняется поиск
    list_filter = ("is_published",)  # Фильтры для списка объектов
    ordering = ("title",)  # Сортировка списка объектов


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    """
    Админ-класс для управления объектами модели Location.
    """
    list_display = ("name", "is_published")  # Поля, отображаемые в списке
    list_editable = ("is_published",)  # Поля, доступные для редактирования в списке
    search_fields = ("name",)  # Поля, по которым выполняется поиск
    list_filter = ("is_published",)  # Фильтры для списка объектов
    ordering = ("name",)  # Сортировка списка объектов


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """
    Админ-класс для управления объектами модели Post.
    """
    list_display = (
        "title",
        "author",
        "pub_date",
        "category",
        "location",
        "is_published",
    )  # Поля, отображаемые в списке
    list_editable = ("is_published", "category", "location")  # Поля для редактирования в списке
    search_fields = (
        "title",
        "text",
        "author__username",
        "category__title",
        "location__name",
    )  # Поля, по которым выполняется поиск
    list_filter = ("is_published", "pub_date", "category", "location")  # Фильтры для списка объектов
    ordering = ("-pub_date",)  # Сортировка списка объектов


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """
    Админ-класс для управления объектами модели Comment.
    """
    list_display = ("post", "author", "created_at")  # Поля, отображаемые в списке
