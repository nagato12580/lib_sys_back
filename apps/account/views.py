from django.shortcuts import render
from datetime import datetime

from django.contrib.admin import action
from django.contrib.auth import hashers, get_user_model
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render
# Create your views here.
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets, mixins, permissions
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenViewBase
from apps.account.models import Account
from .serializers import *

# Create your views here.
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh_token': str(refresh),
        'token': str(refresh.access_token),
    }


class LoginView(APIView):
    """
    post: 登陆，返回token
    """
    def post(self, request):

        username = request.data.get('username', '')
        password = request.data.get('password', '')
        try:
            user = Account.objects.get(username=username)

            if not hashers.check_password(password, user.password):
                return Response({'message': '密码错误'}, status=status.HTTP_400_BAD_REQUEST)
            if not user.is_active:
                return Response({'message': '账号已被冻结'}, status=status.HTTP_400_BAD_REQUEST)
            response_data = get_tokens_for_user(user)
            user.last_login = datetime.now()  # 更新登录时间
            user.save()

        except Account.DoesNotExist:
            return Response({'message': '账号错误'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'data': response_data}, status=status.HTTP_200_OK)


class RegisterViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin
    , mixins.RetrieveModelMixin):
    queryset = Account.objects.all()
    serializer_class = RegisterSerialzier

    def create(self, request, *args, **kwargs):
        with transaction.atomic():
            data = request.data.copy()
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            account_instance = serializer.save()
            response_data = get_tokens_for_user(account_instance)
        headers = self.get_success_headers(serializer.data)
        return Response({'message': '注册成功！',
                         'data': response_data}, status=status.HTTP_201_CREATED, headers=headers)



class MyTokenRefreshView(TokenViewBase):
    """
    自定义刷新token refresh: 刷新token的元素
    """
    serializer_class = CustomTokenRefreshSerializer


class LogoutView(APIView):
    pass