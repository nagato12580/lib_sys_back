from django.shortcuts import render
from django.db.models import Count
# Create your views here.
import json
import uuid
from django.conf import settings
from django.forms.models import model_to_dict
from django.db import transaction
from django.db import transaction
from django.db.models import Q
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, mixins
from utils.common import Pagination

from .models import Press, BookType, Book
from .serializers import *
from .filters import *


# 书籍分类视图
class BookCategoryViewSet(viewsets.ModelViewSet):
	queryset = BookType.objects.filter(is_active=True)
	serializer_class = BookCategorySerializer
	pagination_class = Pagination

	def destroy(self, request, *args, **kwargs):
		instance = self.get_object()
		instance.is_active = False
		instance.save()
		return Response(status=status.HTTP_204_NO_CONTENT)

	@action(methods=['get'], detail=False, url_path='select')
	def get_book_category(self, request):
		queryset = self.get_queryset()
		serializer = BookCategorySelectSerializer(queryset, many=True)
		return Response(serializer.data, status=status.HTTP_200_OK)


# 书籍视图
class BookViewSet(viewsets.ModelViewSet):
	queryset = Book.objects.filter(is_active=True)
	filter_backends = (OrderingFilter, DjangoFilterBackend)
	filter_class = BookFilter
	serializer_class = BookSerializer
	pagination_class = Pagination

	#新增图书
	def create(self, request, *args, **kwargs):
		with transaction.atomic():
			press = request.data.get('press_id')
			serializer = self.get_serializer(data=request.data)
			serializer.is_valid(raise_exception=True)
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)

	def update(self, request, *args, **kwargs):
		# 获取数据
		with transaction.atomic():
			book_bytes = json.dumps(request.data)
			book_dict = json.loads(book_bytes)
			#获取图书分类list
			old=type_list=request.GET.getlist("category_id", 0)
			new = type_list = request.GET.getlist("category_id", 0)
			del book_dict['category_id']
			category = BookType.objects.filter(id__in=category_id)  # 获取更新后图书分类

			partial = kwargs.pop('partial', False)
			instance = self.get_object()
			instance.category.clear()
			instance.category.add(*category)
			serializer = self.get_serializer(instance, data=request.data, partial=partial)
			serializer.is_valid(raise_exception=True)
			self.perform_update(serializer)

			return Response(serializer.data)

	#删除图书
	def destroy(self, request, *args, **kwargs):
		instance = self.get_object()
		instance.is_active = False
		instance.save()
		return Response(status=status.HTTP_204_NO_CONTENT)


	def list(self, request, *args, **kwargs):
		queryset = self.filter_queryset(self.get_queryset())
		page = self.paginate_queryset(queryset)
		if page is not None:
			serializer = self.get_serializer(page, many=True)
			return self.get_paginated_response(serializer.data)

		serializer = self.get_serializer(queryset, many=True)
		return Response(serializer.data)

	# #获取热门图书
	# @action(methods=['get'], detail=True, url_path='popular')
	# def get_popular_book(self, request, pk=None):
	# 	queryset = Book.objects.filter(purchase_id=pk, is_active=True)
	# 	page = self.paginate_queryset(queryset)
	# 	if page is not None:
	# 		serializer = PurchaseBookSerializer(page, many=True)
	# 		return self.get_paginated_response(serializer.data)
	#
	# 	serializer = PurchaseBookSerializer(queryset, many=True)
	# 	return Response(serializer.data)


# 出版社视图
class PressViewSet(viewsets.ModelViewSet):
	queryset = Press.objects.filter(is_active=True)
	serializer_class = PressSerializer
	filter_backends = (OrderingFilter, DjangoFilterBackend)
	filter_class = PressFilter
	pagination_class = Pagination

	def create(self, request, *args, **kwargs):
		pressNo = str(uuid.uuid1()).replace('-', '')[:11]
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		serializer.save(pressNo=pressNo)
		headers = self.get_success_headers(serializer.data)
		return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

	def destroy(self, request, *args, **kwargs):
		instance = self.get_object()
		instance.is_active = False
		instance.save()
		return Response(status=status.HTTP_204_NO_CONTENT)

	@action(methods=['get'], detail=False, url_path='select')
	def get_press(self, request):
		queryset = self.get_queryset()
		serializer = PressSelectSerializer(queryset, many=True)
		return Response(serializer.data, status=status.HTTP_200_OK)

class BorrowViewSet(viewsets.ModelViewSet):
	queryset = Borrow.objects.all()
	serializer_class = BorrowSerializer
	filter_backends = (OrderingFilter, DjangoFilterBackend)
	# filter_class = PressFilter
	pagination_class = Pagination

	def create(self, request, *args, **kwargs):
		new_data = request.data.copy()
		user_id=request.user.id
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		serializer.save(user_id=user_id)
		headers = self.get_success_headers(serializer.data)
		return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


	def list(self, request, *args, **kwargs):
		queryset = self.filter_queryset(self.get_queryset())
		page = self.paginate_queryset(queryset)
		if page is not None:
			serializer = self.get_serializer(page, many=True)
			return self.get_paginated_response(serializer.data)

		serializer = self.get_serializer(queryset, many=True)
		return Response(serializer.data)

	#获取热门书籍排行榜
	@action(methods=['get'], detail=False, url_path='get_popular')
	def get_popular(self, request):

		data=Borrow.objects.values('book_id').annotate(count=Count("id")).order_by('-count').values_list('book_id',flat=True)
		queryset=Book.objects.filter(id__in=list(data))
		queryset = self.filter_queryset(queryset)
		page = self.paginate_queryset(queryset)
		if page is not None:
			serializer = PopularListSerializer(page, many=True, context={'request': request})
			return self.get_paginated_response(serializer.data)
		serializer = PopularListSerializer(queryset, many=True, context={'request': request})
		return Response(serializer.data)
