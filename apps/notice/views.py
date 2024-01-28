from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from apps.account.models import Account
from .serializers import NoticeSerializer
from .models import Notice
from utils.common import Pagination
from .filters import NoticeFilter
# Create your views here.

class NoticetViewSet(ModelViewSet):
    '''社团公告视图'''
    queryset = Notice.objects.filter(is_active=True).select_related('account')
    serializer_class = NoticeSerializer
    pagination_class = Pagination
    filter_class = NoticeFilter
    filter_backends = (OrderingFilter, DjangoFilterBackend)
    ordering_fields = ('id', 'created_time','is_top')
    def create(self, request, *args, **kwargs):
        if not request.user.is_admin() :
            return Response({'message': '您无权限进行新增！'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

