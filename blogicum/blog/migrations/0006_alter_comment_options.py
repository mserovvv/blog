# Generated by Django 3.2.16 on 2024-12-12 17:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_post_comment_count'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ('created_at',), 'verbose_name': 'Комментарий', 'verbose_name_plural': 'Комментарии'},
        ),
    ]
