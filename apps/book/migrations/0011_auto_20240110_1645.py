# Generated by Django 3.2 on 2024-01-10 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0010_auto_20240110_1625'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='book',
            name='unique_ISBN_ISBN',
        ),
        migrations.RemoveField(
            model_name='book',
            name='category',
        ),
        migrations.AddField(
            model_name='book',
            name='category',
            field=models.ManyToManyField(related_name='category_books', to='book.BookType', verbose_name='书籍分类'),
        ),
    ]
