from rest_framework import serializers
from .models import BookMessageTheme
import time
import random
from django.conf import settings
from datetime import date,datetime,timedelta
from .models import Comment,MpttComment
from mptt.models import MPTTModel, TreeForeignKey
from django.conf import settings

class BookMessageThemeSerializer(serializers.ModelSerializer):
    created_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M", required=False, read_only=True)
    updated_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M", required=False, read_only=True)
    is_active = serializers.BooleanField(default=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = BookMessageTheme
        fields = '__all__'
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        # 返回个人信息
        ret['username'] = instance.user.username
        #统计该主题下的回复数
        ret['comment_count']=Comment.objects.filter(message=instance,pre_comment=None,is_active=True).count()
        #楼中楼中楼内容

        return ret

class CommentSerializer(serializers.ModelSerializer):
    created_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M", required=False, read_only=True)
    updated_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M", required=False, read_only=True)
    is_active = serializers.BooleanField(default=True)
    comment_user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Comment
        fields = '__all__'
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        # 返回个人信息
        ret['username'] = instance.comment_user.username
        #统计该评论下的回复数
        ret['comment_count']=Comment.objects.filter(pre_comment=instance,is_active=True).count()
        #构造该评论下的回复树
        ret['comment_tree']=[]
        #一级回复，即对该评论的回复

        return ret

class MpttCommentListSerializer(serializers.ModelSerializer):
    created_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M", required=False, read_only=True)
    updated_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M", required=False, read_only=True)
    is_active = serializers.BooleanField(default=True)
    comment_user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = MpttComment
        fields = '__all__'
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        # 返回个人信息
        ret['username'] = instance.comment_user.username
        ret['wx_photo'] ='{}{}'.format(settings.IMAGE_URL, instance.comment_user.wx_photo)
        #增加以及评论下的二级评论
        ret['reply_count']=instance.get_children().order_by('updated_time').count()
        return ret

from rest_framework import serializers
from .models import BookMessageTheme
import time
import random
from django.conf import settings
from datetime import date,datetime,timedelta
from .models import Comment,MpttComment
from mptt.models import MPTTModel, TreeForeignKey
from django.conf import settings

class BookMessageThemeSerializer(serializers.ModelSerializer):
    created_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M", required=False, read_only=True)
    updated_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M", required=False, read_only=True)
    is_active = serializers.BooleanField(default=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = BookMessageTheme
        fields = '__all__'
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        # 返回个人信息
        ret['username'] = instance.user.username
        #统计该主题下的回复数
        ret['comment_count']=MpttComment.objects.filter(message=instance,is_active=True).count()
        #楼中楼中楼内容

        return ret

class CommentSerializer(serializers.ModelSerializer):
    created_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M", required=False, read_only=True)
    updated_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M", required=False, read_only=True)
    is_active = serializers.BooleanField(default=True)
    comment_user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Comment
        fields = '__all__'
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        # 返回个人信息
        ret['username'] = instance.comment_user.username
        #统计该评论下的回复数
        ret['comment_count']=Comment.objects.filter(pre_comment=instance,is_active=True).count()
        #构造该评论下的回复树
        ret['comment_tree']=[]
        #一级回复，即对该评论的回复

        return ret

class MpttCommentDetailSerializer(serializers.ModelSerializer):
    created_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M", required=False, read_only=True)
    updated_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M", required=False, read_only=True)
    is_active = serializers.BooleanField(default=True)
    comment_user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = MpttComment
        fields = '__all__'
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        # 返回个人信息
        ret['username'] = instance.comment_user.username
        ret['comment_user_id'] = instance.comment_user.id
        ret['wx_photo'] ='{}{}'.format(settings.IMAGE_URL, instance.comment_user.wx_photo)
        ret['childrens']=[]
        #增加以及评论下的二级评论
        childrens=list(instance.get_children().filter(is_active=True).select_related('comment_user').order_by('updated_time').values('id',
                                                                          'comment_content',
                                                                          'created_time','updated_time',
                                                                           'comment_user__wx_photo','comment_user__username','comment_user__id',
                                                                             'reply_to__username'                                            ))
        # dataset=MpttComment.objects.filter(parent=instance).order_by('updated_time').values('id','updated_time')
        for item in childrens:
            #添加头像项
            # item['wx_photo']
            item.pop('updated_time')
            item['comment_user_id'] = item.pop('comment_user__id')
            item['comment_user_username'] = item.pop('comment_user__username')
            item['wx_photo']='{}{}'.format(settings.IMAGE_URL, item.pop('comment_user__wx_photo'))
            item['created_time']=item['created_time'].strftime('%Y-%m-%d %H:%M')
            item['reply_to_username'] = item.pop('reply_to__username')
        ret['reply_count']= len(childrens)
        ret['childrens']=childrens
        ret['childrens_show'] = False
        return ret
