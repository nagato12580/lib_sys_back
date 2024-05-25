from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin

from utils.common import BaseModel


class UserManager(BaseUserManager):
    def _create_user(self, username, password, **kwargs):
        if not username:
            raise ValueError("必须要传递账号")
        if not password:
            raise ValueError("必须要传递密码")
        user = self.model(username=username, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, password, **kwargs):
        return self._create_user(username=username, password=password, **kwargs)

    def create_superuser(self, username, password, **kwargs):
        kwargs.setdefault('is_superuser', True)
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('realname', '管理员')
        if kwargs.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(username=username, password=password, **kwargs)


class Account(AbstractBaseUser, PermissionsMixin):
    telephone = models.CharField(verbose_name='手机号', max_length=20, null=True, blank=True)
    username = models.CharField(verbose_name='用户名', max_length=100, unique=True, null=False, blank=False)
    school_num=models.CharField(verbose_name='学号/工号', max_length=20, null=True, blank=True)
    openid = models.CharField(verbose_name='用户的openid', max_length=200, default='', db_index=True)
    type = models.CharField(verbose_name='用户角色(学生或教职工或校外人员)', max_length=50, default='')
    faculty_title = models.CharField(verbose_name='院系名', max_length=50, null=True)
    realname = models.CharField(verbose_name='姓名', max_length=50, null=True, blank=True)
    is_active = models.BooleanField(verbose_name='账号是否启用', default=True)
    is_staff = models.BooleanField(verbose_name='是否能登陆到后台', default=False)
    can_login_system = models.BooleanField(verbose_name='是否能登陆系统', default=True)
    status = models.CharField(verbose_name='状态', max_length=50, default='')
    grade_name = models.CharField(verbose_name='所在年级名称', max_length=200, default='')
    major_title = models.CharField(verbose_name='专业名称', max_length=50, default='')
    sex = models.CharField(verbose_name='性别', default='', null=True, blank=True, max_length=2)
    wx_photo = models.CharField(verbose_name='微信头像', default='lib_system/wx_photo/216-20240224170703-defalt_avar.png', null=True, blank=True, max_length=350)
    photo = models.ImageField(verbose_name='头像', default='', null=True, blank=True,upload_to='account_photo/')

    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        db_table = "account"
        verbose_name = "账号表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    def is_admin(self):
        """ 判断一个用户是否为超级管理员 """
        if self.is_superuser or self.in_roles(['admin']):
            return True
        return False




