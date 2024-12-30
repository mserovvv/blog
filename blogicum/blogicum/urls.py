from django.contrib import admin
from django.urls import include, path, reverse_lazy
from django.views.generic import CreateView

from .forms import CustomUserCreationForm

# Обработчики ошибок
handler404 = "pages.views.page_not_found"  # Пользовательская страница ошибки 404
handler500 = "pages.views.server_error"  # Пользовательская страница ошибки 500

urlpatterns = [
    path("", include("blog.urls", namespace="blog")),  # Маршруты для приложения блога
    path("admin/", admin.site.urls),  # Административная панель Django
    path("auth/", include("django.contrib.auth.urls")),  # Стандартные маршруты аутентификации Django
    path(
        "auth/registration/",
        CreateView.as_view(
            template_name="registration/registration_form.html",  # Шаблон для формы регистрации
            form_class=CustomUserCreationForm,  # Кастомная форма регистрации
            success_url=reverse_lazy("blog:index"),  # Перенаправление после успешной регистрации
        ),
        name="registration",
    ),
    path("pages/", include("pages.urls", namespace="pages")),  # Маршруты для статических страниц
]
