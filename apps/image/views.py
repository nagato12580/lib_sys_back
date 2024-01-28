from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from rest_framework import mixins, viewsets, status
from rest_framework.viewsets import GenericViewSet
from django.shortcuts import render
from utils.common import Pagination


from .models import *
from .serializers import *

# Create your views here.

class ClubSwiperViewSet(mixins.CreateModelMixin,
                        mixins.DestroyModelMixin,
                        mixins.ListModelMixin,
                        GenericViewSet):
    queryset = LibSwiper.objects.all().order_by('id')
    serializer_class = LibSwiperSerializer
    filter_backends = (OrderingFilter, DjangoFilterBackend)
    pagination_class = Pagination
    ordering_fields = ('id', 'created_time')
    filter_fields = ['is_active']

    def create(self, request, *args, **kwargs):
        if not request.user.is_admin() :
            return Response({'message': '您无权限进行新增！'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)