from django.shortcuts import render
from django.views.generic import TemplateView


class AboutView(TemplateView):
    """
    Представление для отображения страницы "О нас".
    """

    template_name = "pages/about.html"


class RulesView(TemplateView):
    """
    Представление для отображения страницы "Правила".
    """

    template_name = "pages/rules.html"


def csrf_failure(request, reason=""):
    """
    Обработчик ошибки CSRF.
    """
    return render(request, "pages/403csrf.html", status=403)


def page_not_found(request, exception):
    """
    Обработчик ошибки 404 (страница не найдена).
    """
    return render(request, "pages/404.html", status=404)


def server_error(request):
    """
    Обработчик ошибки 500 (внутренняя ошибка сервера).
    """
    return render(request, "pages/500.html", status=500)
