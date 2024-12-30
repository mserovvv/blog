from django.contrib.auth.mixins import UserPassesTestMixin


class OnlyAuthorMixin(UserPassesTestMixin):
    """
    Миксин для проверки, что текущий пользователь является автором объекта.
    """

    def test_func(self):
        """
        Проверяет, является ли текущий пользователь автором объекта.
        """
        obj = self.get_object()
        return obj.author == self.request.user

    def handle_no_permission(self):
        """
        Обрабатывает ситуацию, когда у пользователя нет прав доступа.
        Перенаправляет на страницу с деталями поста.
        """
        obj = self.get_object()
        from django.shortcuts import redirect

        return redirect("blog:post_detail", pk=obj.pk)
