import django_filters
import django_filters
from rest_framework import filters
from .models import Notice


class NoticeFilter(django_filters.rest_framework.FilterSet):
    id=django_filters.CharFilter()
    account_id = django_filters.CharFilter()
    is_active=django_filters.BooleanFilter()
    is_top = django_filters.BooleanFilter()
    class Meta:
        model = Notice
        fields = ['id','account_id', 'is_active', 'is_top']