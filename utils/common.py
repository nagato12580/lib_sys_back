from rest_framework.pagination import PageNumberPagination
from django.db import models


class Pagination(PageNumberPagination):
    """ 分页设置 """
    page_size_query_param = 'limit'
    page_query_param = 'page'



class BaseModel(models.Model):
    """
    用于model类，为每个model新增创建时间和更新时间字段
    """
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间', null=True)
    updated_time = models.DateTimeField(auto_now=True, verbose_name='更新时间', null=True)

    class Meta:
        abstract = True


class CustomError(Exception):
    """
    自定义异常，用于excel表，reason表示异常信息
    """
    def __init__(self, reason):
        self.reason = reason

def process_view(request):
    csrf_token=request.META.get('CSRF_COOKIE')#获取请求头里的
    if csrf_token is None:
        return