from django.conf import settings
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import serializers, status
from .models import Faculty,Major

class FacultySerializer(serializers.ModelSerializer):
    class Meta:
        model = Faculty
        fields = '__all__'

class MajorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Major
        fields = '__all__'

