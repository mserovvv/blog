from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views
from .views import (
    PostCreateView,
    PostDeleteView,
    PostDetailView,
    PostUpdateView,
    UserUpdateView,
    profile_view,
)

app_name = "blog"  # Указывает пространство имен для приложения "blog".

# Список URL-маршрутов приложения
urlpatterns = [
    path("", views.index, name="index"),  # Главная страница блога.
    path(
        "category/<slug:category_slug>/",
        views.category_posts,
        name="category_posts"  # Посты, относящиеся к определенной категории.
    ),
    path("posts/create/", PostCreateView.as_view(), name="create_post"),  # Создание нового поста.
    path("posts/<int:pk>/comment/", views.add_comment, name="add_comment"),  # Добавление комментария.
    path(
        "posts/<int:pk>/edit_comment/<int:comment_id>/",
        views.edit_comment,
        name="edit_comment"  # Редактирование существующего комментария.
    ),
    path(
        "posts/<int:pk>/delete_comment/<int:comment_id>/",
        views.delete_comment,
        name="delete_comment"  # Удаление комментария.
    ),
    path("posts/<int:pk>/edit/", PostUpdateView.as_view(), name="edit_post"),  # Редактирование поста.
    path(
        "posts/<int:pk>/delete/",
        PostDeleteView.as_view(),
        name="delete_post"  # Удаление поста.
    ),
    path("posts/<int:pk>/", PostDetailView.as_view(), name="post_detail"),  # Просмотр деталей поста.
    path("profile/edit/", UserUpdateView.as_view(), name="edit_profile"),  # Редактирование профиля.
    path("profile/<str:username>/", profile_view, name="profile"),  # Просмотр профиля пользователя.
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # Обработка медиафайлов в режиме разработки.
