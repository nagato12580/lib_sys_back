import django_filters
from rest_framework import filters
from django.db.models import Q
from apps.message.models import BookMessageTheme,Comment,MpttComment
class BookMessageThemeFilter(django_filters.rest_framework.FilterSet):
    book_id = django_filters.CharFilter()
    user_id = django_filters.CharFilter()
    id=django_filters.CharFilter()
    class Meta:
        model = BookMessageTheme
        fields = ['id','book_id', 'user_id']

class CommentFilter(django_filters.rest_framework.FilterSet):
    message_id = django_filters.CharFilter()
    comment_user = django_filters.CharFilter()
    class Meta:
        model = Comment
        fields = ['message_id', 'comment_user']


class MpttCommentFilter(django_filters.rest_framework.FilterSet):
    message_id = django_filters.CharFilter()
    parent_id = django_filters.CharFilter()
    class Meta:
        model = MpttComment
        fields = ['message_id', 'parent_id']