# Generated by Django 3.2 on 2024-01-23 21:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0017_book_checkedoutbooks'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='bookLocation',
            field=models.CharField(default=1, max_length=40, verbose_name='藏书地址'),
            preserve_default=False,
        ),
    ]