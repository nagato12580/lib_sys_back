from django.db import models
from apps.account.models import Account
from utils.common import BaseModel

# Create your models here.

class Notice(BaseModel):
    title = models.CharField(verbose_name='公告标题', max_length=100)
    content = models.TextField(verbose_name='公告内容')
    file = models.JSONField(verbose_name='公告文件',blank=True,null=True)
    account = models.ForeignKey(Account, verbose_name='申请人', related_name='account_notice',
                                null=True, blank=True, on_delete=models.CASCADE)
    is_active = models.BooleanField(verbose_name='是否启用', default=True)
    is_top = models.BooleanField(verbose_name='是否顶置', default=False)

    class Meta:
        db_table = "notice"
        verbose_name = "公告表"
        verbose_name_plural = verbose_name