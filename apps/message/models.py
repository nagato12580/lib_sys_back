from django.db import models

# Create your models here.

from django.db import models
# Create your models here.
from utils.common import BaseModel
from apps.book.models import Book
from apps.account.models import Account
from mptt.models import MPTTModel, TreeForeignKey
class BookMessageTheme(BaseModel):
    book = models.ForeignKey(Book, verbose_name='相关图书', related_name='message', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    title=models.CharField(verbose_name='主题', max_length=50)
    content=models.CharField(verbose_name='内容', max_length=200)
    user = models.ForeignKey(Account, verbose_name='发起人', related_name='book_message', on_delete=models.DO_NOTHING)

class Meta:
    db_table = "book_message_theme"
    verbose_name = "图书留言主题"
    verbose_name_plural = verbose_name


class Comment(BaseModel):  # 定义评论模型
    message = models.ForeignKey(to=BookMessageTheme, on_delete=models.DO_NOTHING, verbose_name='评论文章',related_name='all_comments')
    comment_content = models.TextField(verbose_name='评论内容')
    is_active = models.BooleanField(default=True)
    comment_user = models.ForeignKey(to=Account, on_delete=models.DO_NOTHING, verbose_name='评论者',related_name='user_comments')
    pre_comment = models.ForeignKey('self', on_delete=models.DO_NOTHING, null=True,
                                    verbose_name='父评论id')  # 父级评论，如果没有父级则为空NULL, "self"表示外键关联自己

    class Meta:
        db_table = 'message_comment'
        verbose_name = '留言评论'
        verbose_name_plural = verbose_name


class MpttComment(MPTTModel):  # 定义评论模型
    message = models.ForeignKey(to=BookMessageTheme, on_delete=models.DO_NOTHING, verbose_name='评论文章',related_name='all_mptt_comments')
    comment_content = models.TextField(verbose_name='评论内容')
    is_active = models.BooleanField(default=True)
    comment_user = models.ForeignKey(to=Account, on_delete=models.DO_NOTHING, verbose_name='评论者',related_name='user_mptt_comments')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间', null=True)
    updated_time = models.DateTimeField(auto_now=True, verbose_name='更新时间', null=True)

    # 新增，mptt树形结构
    parent  = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
        verbose_name = '父评论id'
    )

    # 新增，记录二级评论回复给谁, str
    reply_to = models.ForeignKey(
        Account,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='replyers'
    )


    class MPTTMeta:
        db_table = 'mptt_comment'
        verbose_name = 'mptt留言评论'
        verbose_name_plural = verbose_name
        order_insertion_by = ['created_time']

