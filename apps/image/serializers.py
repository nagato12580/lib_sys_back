from django.conf import settings
from rest_framework import serializers

from .models import LibSwiper

class LibSwiperSerializer(serializers.ModelSerializer):
    created_time = serializers.DateTimeField(format="%Y-%m-%d", required=False, read_only=True)
    updated_time = serializers.DateTimeField(format="%Y-%m-%d", required=False, read_only=True)

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['full_image_path'] = [{'url': f"{settings.IMAGE_URL}{file.get('data')}", 'name': file.get('file_name')}
                                  for file in instance.cover]

        return ret

    class Meta:
        model = LibSwiper
        fields = '__all__'
