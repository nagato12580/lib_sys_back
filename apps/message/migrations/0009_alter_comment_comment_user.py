# Generated by Django 3.2 on 2024-04-18 22:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('message', '0008_alter_bookmessagetheme_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='comment_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_comments', to=settings.AUTH_USER_MODEL, verbose_name='评论者'),
        ),
    ]