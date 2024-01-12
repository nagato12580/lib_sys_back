from rest_framework import serializers
from .models import *
import time
import random
from django.conf import settings
from datetime import date

# 出版社序列化器
class PressSerializer(serializers.ModelSerializer):
	is_active = serializers.BooleanField(default=True)

	class Meta:
		model = Press
		fields = '__all__'


# 图书类别序列化器
class BookCategorySerializer(serializers.ModelSerializer):
	is_active = serializers.BooleanField(default=True)

	class Meta:
		model = BookType
		fields = '__all__'


# 图书序列化器
class BookSerializer(serializers.ModelSerializer):
	is_active = serializers.BooleanField(default=True)
	stockNumber = serializers.IntegerField(default=0)


	def to_representation(self, instance):
		ret = super().to_representation(instance)
		ret['pressTitle'] = instance.press.pressTitle
		ret['image_url'] = '{}{}'.format(settings.IMAGE_URL, instance.image)
		category_detail = []
		category_id = []
		for book_category in instance.category.all():
			category_detail.append(book_category.name)
			category_id.append(book_category.id)
		ret['category_detail'] = category_detail
		return ret

	class Meta:
		model = Book
		exclude = ('category',)


# 出版社选择器
class PressSelectSerializer(serializers.ModelSerializer):
	class Meta:
		model = Press
		fields = ('id', 'pressTitle')
		# fields = '__all__'


# 书籍选择器
class BookCategorySelectSerializer(serializers.ModelSerializer):
	class Meta:
		model = BookType
		fields = ('id', 'name')



class BorrowSerializer(serializers.ModelSerializer):
	user=serializers.CharField(read_only=True)#只读，序列化时候无需验证

	def create(self, validated_data):
		return Borrow.objects.create(**validated_data)

	def validate(self, attrs):
		#验证归还日期
		if attrs['return_data']:
			today=date.today()
			if attrs['return_data'] <= today:
				raise serializers.ValidationError(detail="归还日期不能早于今天")
			d=attrs['return_data']-today
			if d.days>90:
				raise serializers.ValidationError(detail="借阅天数不得大于90天")
		return attrs
	class Meta:
		model = Borrow
		fields = '__all__'


class PopularListSerializer(serializers.ModelSerializer):
	class Meta:
		model=Book
		fields = ('id','bookTitle','author','introduction','image')

	def to_representation(self, instance):
		ret = super().to_representation(instance)
		ret['image']='{}{}'.format(settings.IMAGE_URL, instance.image)
		return ret
