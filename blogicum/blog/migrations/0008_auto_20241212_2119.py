# Generated by Django 3.2.16 on 2024-12-12 18:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_alter_post_is_published'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='is_scheduled',
            field=models.BooleanField(default=False, help_text='Автоматически публикует пост, если наступила дата публикации.', verbose_name='Публикация по расписанию'),
        ),
        migrations.AlterField(
            model_name='post',
            name='is_published',
            field=models.BooleanField(default=False, help_text='Определяет, виден ли пост на сайте.', verbose_name='Опубликован'),
        ),
    ]
