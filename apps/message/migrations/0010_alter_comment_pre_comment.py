# Generated by Django 3.2 on 2024-04-18 22:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('message', '0009_alter_comment_comment_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='pre_comment',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='message.comment', verbose_name='父评论id'),
        ),
    ]