from rest_framework import serializers
from .models import Reservation,Seat
from django.conf import settings

class SeatSerializer(serializers.ModelSerializer):
    created_time = serializers.DateTimeField(format="%Y-%m-%d", required=False, read_only=True)
    updated_time = serializers.DateTimeField(format="%Y-%m-%d ", required=False, read_only=True)
    is_active=serializers.BooleanField(default=True)
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        return ret

    class Meta:
        model = Seat
        fields = '__all__'

class ReservationSerializer(serializers.ModelSerializer):
    created_time = serializers.DateTimeField(format="%Y-%m-%d", required=False, read_only=True)
    updated_time = serializers.DateTimeField(format="%Y-%m-%d ", required=False, read_only=True)
    is_active=serializers.BooleanField(default=True)
    user = serializers.HiddenField(  # 默认为当前创建者
        default=serializers.CurrentUserDefault()
    )
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        return ret

    class Meta:
        model = Reservation
        fields = '__all__'