# Generated by Django 3.2 on 2024-04-18 22:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('book', '0022_remove_press_pressno'),
    ]

    operations = [
        migrations.AlterField(
            model_name='borrow',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='books', to=settings.AUTH_USER_MODEL, verbose_name='借阅人'),
        ),
    ]
