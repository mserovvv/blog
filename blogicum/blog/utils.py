from django.core.paginator import Paginator


def paginate_queryset(queryset, request, per_page):
    """
    Пагинация для переданного набора данных (queryset).
    """
    paginator = Paginator(queryset, per_page)  # Создаём объект пагинатора.
    page_number = request.GET.get("page")  # Получаем номер текущей страницы из параметров запроса.
    return paginator.get_page(page_number)  # Возвращаем объект текущей страницы.
