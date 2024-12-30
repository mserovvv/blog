# Generated by Django 3.2.16 on 2024-12-12 18:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_alter_comment_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='is_published',
            field=models.BooleanField(default=False, help_text='Отметьте, если пост должен быть видимым на сайте.', verbose_name='Опубликован'),
        ),
    ]
