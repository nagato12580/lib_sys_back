from django.conf import settings
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import serializers, status
from .models import Account

class AccountSerializer(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True)
    class Meta:
        model = Account
        fields = '__all__'
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['wx_photo'] = '{}{}'.format(settings.IMAGE_URL, instance.wx_photo)
        return ret



class CustomTokenRefreshSerializer(serializers.Serializer):
    """
    自定义刷新token返回的数据
    """
    refresh = serializers.CharField()

    def validate(self, attrs):
        refresh = RefreshToken(attrs['refresh'])

        data = {'token': str(refresh.access_token)}

        if api_settings.ROTATE_REFRESH_TOKENS:
            if api_settings.BLACKLIST_AFTER_ROTATION:
                try:
                    # Attempt to blacklist the given refresh token
                    refresh.blacklist()
                except AttributeError:
                    # If blacklist app not installed, `blacklist` method will
                    # not be present
                    pass

            refresh.set_jti()
            refresh.set_exp()

            data['refresh'] = str(refresh)

        return data


class RegisterSerialzier(serializers.ModelSerializer):
    password1 = serializers.CharField(max_length=20, min_length=8, write_only=True, allow_null=False)

    # code = serializers.CharField(read_only=True,write_only=False,)
    def validate(self, attrs):
        password = attrs['password']
        password1 = attrs['password1']
        if password != password1:
            raise serializers.ValidationError('两次输入的密码不一致')
        return attrs

    def create(self, validated_data):
        password1 = validated_data.pop('password1')
        return Account.objects.create_user(**validated_data)

    class Meta:
        model = Account
        fields = ('username', 'password', 'password1',)
        extra_kwargs = {
            'password': {'min_length': 8, 'max_length': 20, 'required': True},
            'username': {'min_length': 5, 'max_length': 20, 'required': True},
            'mobile': {'min_length': 11, 'max_length': 11, 'required': True},
        }

    def to_internal_value(self, data):
        # 进提取所需要的数据，对其进行反序列化，data代表未验证的数据
        new_data = {
            'username': data['username'],
            'password': data['password'],
            'password1': data['password1'],
        }
        return super().to_internal_value(new_data)