# Generated by Django 3.2 on 2024-03-01 11:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('book', '0021_borrow_borrowing_date'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BookMessageTheme',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(auto_now_add=True, null=True, verbose_name='创建时间')),
                ('updated_time', models.DateTimeField(auto_now=True, null=True, verbose_name='更新时间')),
                ('is_active', models.BooleanField(default=True)),
                ('title', models.CharField(max_length=50, verbose_name='主题')),
                ('content', models.CharField(max_length=200, verbose_name='内容')),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='message', to='book.book', verbose_name='相关图书')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='book_message', to=settings.AUTH_USER_MODEL, verbose_name='发起人')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_content', models.TextField(verbose_name='评论内容')),
                ('is_active', models.BooleanField(default=True)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='all_comments', to='message.bookmessagetheme', verbose_name='评论文章')),
                ('comment_user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='user_comments', to=settings.AUTH_USER_MODEL, verbose_name='评论者')),
                ('pre_comment', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='message.comment', verbose_name='父评论id')),
            ],
            options={
                'verbose_name': '留言评论',
                'verbose_name_plural': '留言评论',
                'db_table': 'message_comment',
            },
        ),
    ]
