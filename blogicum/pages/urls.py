from django.urls import path

from . import views

app_name = 'pages'  # Указывает пространство имен для приложения "pages".

urlpatterns = [
    path('about/', views.AboutView.as_view(), name='about'),  # Маршрут для страницы "О нас".
    path('rules/', views.RulesView.as_view(), name='rules'),  # Маршрут для страницы "Правила".
]
