# Generated by Django 3.2 on 2024-01-10 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0012_borrow'),
    ]

    operations = [
        migrations.AddField(
            model_name='borrow',
            name='total_return_data',
            field=models.DateField(blank=True, null=True, verbose_name='实际归还日期'),
        ),
        migrations.AlterField(
            model_name='borrow',
            name='return_data',
            field=models.DateField(verbose_name='预计归还日期'),
        ),
    ]
