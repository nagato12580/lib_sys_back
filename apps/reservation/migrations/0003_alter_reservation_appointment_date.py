# Generated by Django 3.2 on 2024-03-11 16:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0002_alter_reservation_period'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='appointment_date',
            field=models.DateField(verbose_name='预约日期'),
        ),
    ]
