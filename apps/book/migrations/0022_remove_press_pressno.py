# Generated by Django 3.2 on 2024-04-10 21:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0021_borrow_borrowing_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='press',
            name='pressNo',
        ),
    ]
