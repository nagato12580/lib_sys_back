from rest_framework import serializers
from .models import Notice
from django.conf import settings

class NoticeSerializer(serializers.ModelSerializer):
    created_time = serializers.DateTimeField(format="%Y-%m-%d", required=False, read_only=True)
    updated_time = serializers.DateTimeField(format="%Y-%m-%d ", required=False, read_only=True)
    is_active=serializers.BooleanField(default=True)
    account = serializers.HiddenField(  # 默认为当前创建者
        default=serializers.CurrentUserDefault()
    )
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        # 返回个人信息
        ret['realname'] = instance.account.realname
        #返回文件数据
        ret['full_image_path']=None
        if instance.file!=None:
            ret['full_image_path'] = [{'url': f"{settings.IMAGE_URL}{file.get('data')}", 'name': file.get('file_name')}
                                      for file in instance.file]
        return ret

    class Meta:
        model = Notice
        fields = '__all__'