from django.shortcuts import render
from datetime import datetime
from utils.common import Pagination
from django.contrib.admin import action
from django.contrib.auth import hashers, get_user_model
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render
from django.conf import settings
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
# from rest_framework_simplejwt.views import TokenViewBase
from apps.account.models import Account
from .serializers import *
from utils.function import create_string_number
import requests
import json

def get_openid(code):
    """ 微信根据code 获取openid"""

    url = f"https://api.weixin.qq.com/sns/jscode2session?appid={settings.APP_ID}&secret={settings.APP_SECRET}&js_code" \
          f"={code}&grant_type=authorization_code"
    result = requests.get(url)
    res = json.loads(result.text)  # 得到的数据格式为：{'session_key': '', 'openid': ''}
    openid = res.get('openid', None)
    return openid

# Create your views here.
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh_token': str(refresh),
        'token': str(refresh.access_token),
    }

#测试用
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

#微信小程序登录
class WechatLoginView(APIView):

    def post(self, request):
        """ 微信登陆 """
        code = request.data.get('code', None)
        if not code:
            return Response({'message': '缺少code'}, status=status.HTTP_400_BAD_REQUEST)
        openid = get_openid(code)
        if not openid:
            return Response({'message': '请求微信服务器失败，请重试'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        #获取用户
        user = Account.objects.filter(openid=openid)
        #用户不存在就创建一个用户
        if not user:
         user = Account.objects.create(
            username='微信用户'+create_string_number(6),
            openid=openid,
        )
        else:
            user=Account.objects.get(openid=openid)

        data = get_tokens_for_user(user)
        user.last_login = datetime.now()  # 修改该账号的最近登陆时间
        user.save()
        data['account_id']=user.id
        data['openid'] = openid
        data['faculty'] = user.faculty_title
        data['username'] = user.username
        data['realname'] = user.realname
        data['wx_photo'] = '{}{}'.format(settings.IMAGE_URL, user.wx_photo)
        return Response({'data': data, 'message': '登录成功'}, status=status.HTTP_200_OK)


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



# class MyTokenRefreshView(TokenViewBase):
#     """
#     自定义刷新token refresh: 刷新token的元素
#     """
#     serializer_class = CustomTokenRefreshSerializer


class LogoutView(APIView):
    pass

class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.filter(is_active=True)
    filter_backends = (OrderingFilter, DjangoFilterBackend)
    # filter_class = BookFilter
    serializer_class = AccountSerializer
    pagination_class = Pagination

    #修改用户名和头像接口
    @action(methods=['post'], detail=False, url_path='update_userinfo')
    def update_userinfo(self,request):
        username = request.data.get('username', '')
        avatar = request.data.get('avatar', '')
        user=request.user
        if username:
            user.username=username
        if avatar:
            user.wx_photo=avatar
        user.save()

        return Response({
            'username':user.username,
            'wx_photo':'{}{}'.format(settings.IMAGE_URL, user.wx_photo)
        }, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False, url_path='get_userinfo')
    def get_userinfo(self, request):
        user = request.user
        account_id=user.id
        instance=Account.objects.get(id=account_id)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(methods=['post'], detail=False, url_path='comfirm_info')
    def comfirm_info(self, request):
        user_id=request.user.id
        myFacult = request.data.get('myFacult', '')
        myGrade=request.data.get('myGrade', '')
        myMajor=request.data.get('myMajor', '')
        realName=request.data.get('realName', '')
        telephone=request.data.get('telephone', '')
        if not all([myFacult, myGrade,myMajor,realName,telephone]):
            return Response({'message': '缺少参数'}, status=status.HTTP_400_BAD_REQUEST)
        #更新信息
        Account.objects.filter(id=user_id).update(
            faculty_title=myFacult,
            realname=realName,
            telephone=telephone,
            major_title=myMajor,
            grade_name=myGrade
        )
        return Response(status=status.HTTP_200_OK)

    #用于检查资料是否完善
    @action(methods=['get'], detail=False, url_path='check_userinfo')
    def check_userinfo(self, request):
        user = request.user
        account_id=user.id
        instance=Account.objects.get(id=account_id)

        realname=instance.realname
        telephone=instance.telephone
        faculty_title=instance.faculty_title
        grade_name=instance.grade_name
        major_title=instance.major_title
        if not all([realname, telephone,faculty_title,grade_name,major_title]):
            return Response(status=status.HTTP_200_OK,data={"flage":False})
        else:
            return Response(status=status.HTTP_200_OK,data={"flage":True})

    @action(methods=['get'], detail=False, url_path='check_login')
    def check_login(self, request):
        user = request.user
        account_id=user.id
        if account_id:
            return Response(status=status.HTTP_200_OK, data={"isLogin": True})
        else:
            return Response(status=status.HTTP_200_OK, data={"isLogin": False})








