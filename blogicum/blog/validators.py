from datetime import date

from django.core.exceptions import ValidationError


def real_year(value) -> None:
    """
    Валидатор для проверки, что дата поста не находится в прошлом.
    """
    if value.date() < date.today():
        raise ValidationError("Нельзя делать пост в прошлом")
