# Generated by Django 3.2 on 2024-01-23 21:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0016_alter_booktype_root_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='checkedOutBooks',
            field=models.IntegerField(default=0, verbose_name='已借出图书数量'),
        ),
    ]
