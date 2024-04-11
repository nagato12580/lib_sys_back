# Generated by Django 3.2 on 2024-04-11 16:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('message', '0005_rename_pre_comment_mpttcomment_parent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mpttcomment',
            name='message',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='all_mptt_comments', to='message.bookmessagetheme', verbose_name='评论文章'),
        ),
    ]
