# Generated by Django 3.2 on 2024-02-25 15:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('book', '0018_book_booklocation'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookCollection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(auto_now_add=True, null=True, verbose_name='创建时间')),
                ('updated_time', models.DateTimeField(auto_now=True, null=True, verbose_name='更新时间')),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='star_user', to='book.book', verbose_name='借阅图书')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='star_book', to=settings.AUTH_USER_MODEL, verbose_name='借阅人')),
            ],
            options={
                'verbose_name': '图书收藏',
                'verbose_name_plural': '图书收藏',
                'db_table': 'collection',
            },
        ),
    ]