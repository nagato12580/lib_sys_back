from django.shortcuts import render
from django.db.models import Count
# Create your views here.
import json
import uuid
import datetime
from django.conf import settings
from django.forms.models import model_to_dict
from django.db import transaction
from django.db import transaction
from django.db.models import F, Q
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, mixins
from utils.common import Pagination

from django.db.models import Case, When, Value, IntegerField
from .models import Press, BookType, Book,BookCollection
from .serializers import *
from .filters import *


# 书籍一级分类视图
class BookRootCategoryViewSet(viewsets.ModelViewSet):
	queryset = BookRootType.objects.filter(is_active=True)
	serializer_class = BookRootCategorySerializer
	pagination_class = Pagination
	def destroy(self, request, *args, **kwargs):
		instance = self.get_object()
		instance.is_active = False
		instance.save()
		return Response(status=status.HTTP_204_NO_CONTENT)

	@action(methods=['get'], detail=False, url_path='select')
	def get_book_second_category(self, request):
		root_id=request.GET.get('root')
		queryset = BookRootType.objects.select_related().filter(id=root_id,is_active=True)
		serializer = BookRootCategorySelectSerializer(queryset, many=True)
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
		queryset = self.filter_queryset(self.get_queryset().order_by('-created_time'))
		page = self.paginate_queryset(queryset)
		if page is not None:
			serializer = BookListSerializer(page, many=True)
			return self.get_paginated_response(serializer.data)

		serializer = BookListSerializer(queryset, many=True)
		return Response(serializer.data)

	#获取新上架图书排行榜
	@action(methods=['get'], detail=False, url_path='get_new_book')
	def get_new_book(self, request):
		queryset=Book.objects.filter(is_active=True).order_by('-created_time')
		queryset = self.filter_queryset(queryset)
		page = self.paginate_queryset(queryset)
		if page is not None:
			serializer = BookListSerializer(page, many=True)
			return self.get_paginated_response(serializer.data)
		serializer = BookListSerializer(queryset, many=True)
		return Response(serializer.data)

	@action(methods=['get'], detail=False, url_path='search')
	def search(self, request, *args, **kwargs):
		key=request.GET.get("value",'')
		if not key:
			return Response([],status.HTTP_204_NO_CONTENT)
		else:
			queryset=Book.objects.filter(Q(bookTitle__icontains=key) | Q(author__icontains=key))
			page = self.paginate_queryset(queryset)
			if page is not None:
				serializer = BookListSerializer(page, many=True)
				return self.get_paginated_response(serializer.data)

			serializer = BookListSerializer(queryset, many=True)
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

	#借阅图书
	def create(self, request, *args, **kwargs):
		new_data = request.data.copy()
		book_id=request.data.get('book')
		user_id=request.user.id
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		serializer.save(user_id=user_id)
		book=Book.objects.get(id=book_id)
		#不够借
		if book.stockNumber-book.checkedOutBooks<=0:
			return Response(status=status.HTTP_400_BAD_REQUEST)
		book.checkedOutBooks=book.checkedOutBooks+1
		book.save()
		return Response(serializer.data, status=status.HTTP_201_CREATED)

	#归还图书
	@action(methods=['post'], detail=False, url_path='returned')
	def returned(self, request):
		user = request.user
		if not user.id:
			return Response({'message': '请先登录'}, status=status.HTTP_400_BAD_REQUEST)
		book_id=request.data.get('book_id')
		# 获取当前日期
		today = datetime.now().date()
		#更新借阅信息
		book=Book.objects.get(id=book_id)
		borrow=Borrow.objects.filter(user=user,book=book,is_return=False).first()
		borrow.is_return=True
		borrow.total_return_data = today
		borrow.save()
		#更新图书馆藏信息
		checkedOutBooks=book.checkedOutBooks
		book.checkedOutBooks=checkedOutBooks-1
		book.save()
		return Response(status=status.HTTP_200_OK)

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
		queryset=Book.objects.filter(id__in=list(data),is_active=True)
		queryset = self.filter_queryset(queryset)
		page = self.paginate_queryset(queryset)
		if page is not None:
			serializer = PopularListSerializer(page, many=True, context={'request': request})
			return self.get_paginated_response(serializer.data)
		serializer = PopularListSerializer(queryset, many=True, context={'request': request})
		return Response(serializer.data)


	#查看我的借阅
	@action(methods=['get'], detail=False, url_path='get_my_borrow')
	def get_my_borrow(self, request):
		user = request.user
		if not user.id:
			return Response({'message': '请先登录'}, status=status.HTTP_400_BAD_REQUEST)
		#未归还图书
		book_list_no = list(
			Borrow.objects.select_related('book').filter(user=user,is_return=False).order_by('borrowing_date').values('book_id','book__ISBN','book__image','book__author',
																									'book__bookTitle','book__introduction',
																									'return_data','total_return_data',
																									'borrowing_date'))
		res_no=[]
		item={}
		for book in book_list_no:
			item={
				'id':book['book_id'],
				'image':'{}{}'.format(settings.IMAGE_URL, book['book__image']),
				'ISBN':book['book__ISBN'],
				'bookTitle':book['book__bookTitle'],
				'author': book['book__author'],
				'introduction': book['book__introduction'],
				'borrowing_date':book['borrowing_date'],
				'return_data': book['return_data'],
				'total_return_data': book['total_return_data'],
			}
			res_no.append(item)

		#已归还图书
		book_list = list(
			Borrow.objects.select_related('book').filter(user=user,is_return=True).order_by('borrowing_date').values('book_id','book__image','book__author',
																									'book__bookTitle','book__introduction',
																									'return_data','total_return_data',
																												   'borrowing_date'))
		res=[]
		for book in book_list:
			item={
				'id':book['book_id'],
				'image':'{}{}'.format(settings.IMAGE_URL, book['book__image']),
				'bookTitle':book['book__bookTitle'],
				'author': book['book__author'],
				'introduction': book['book__introduction'],
				'borrowing_date': book['borrowing_date'],
				'return_data': book['return_data'],
				'total_return_data': book['total_return_data'],
			}
			res.append(item)
		return Response({'no_returned':res_no,'returned':res},status=status.HTTP_200_OK)


class BookCollectionViewSet(viewsets.ModelViewSet):
	queryset = BookCollection.objects.all()
	serializer_class = BookCollectionSerializer
	filter_backends = (OrderingFilter, DjangoFilterBackend)
	# filter_class = PressFilter
	pagination_class = Pagination

	#新增收藏
	def create(self, request, *args, **kwargs):
		user = request.user
		book_id = request.data.get('book_id')
		if  not user.id:
			return Response({'message':'请先登录'},status=status.HTTP_400_BAD_REQUEST)
		collection=BookCollection.objects.filter(user=user,book_id=book_id)
		if not collection:
			BookCollection.objects.create(user=user,book_id=book_id)
			return Response({'isStar':True},status=status.HTTP_200_OK)
		else:
			collection.update(is_active=True)
			return Response({'isStar': True}, status=status.HTTP_200_OK)

	#获取当前图书收藏状态
	@action(methods=['get'], detail=False, url_path='get_status')
	def get_status(self, request):
		user = request.user
		book_id = request.GET.get('book_id')
		if not user.id:
			return Response({'message':'请先登录'},status=status.HTTP_400_BAD_REQUEST)
		collection=BookCollection.objects.filter(user=user,book_id=book_id,is_active=True)
		if collection:
			return Response({'isStar':True},status=status.HTTP_200_OK)
		else:
			return Response({'isStar':False},status=status.HTTP_200_OK)

	#取消收藏
	@action(methods=['post'], detail=False, url_path='cancel')
	def cancel(self, request):
		user = request.user
		book_id = request.data.get('book_id')
		if not user.id:
			return Response({'message':'请先登录'},status=status.HTTP_400_BAD_REQUEST)
		collection=BookCollection.objects.filter(user=user,book_id=book_id,is_active=True)
		if collection:
			BookCollection.objects.filter(user=user,book_id=book_id,is_active=True).update(is_active=False)
			return Response({'isStar':False},status=status.HTTP_200_OK)
		else:
			return Response({'isStar':True},status=status.HTTP_200_OK)


	#查看我的收藏列表
	def list(self, request, *args, **kwargs):
		user = request.user
		if not user.id:
			return Response({'message':'请先登录'},status=status.HTTP_400_BAD_REQUEST)
		book_list = list(BookCollection.objects.filter(user=user,is_active=True).order_by('updated_time').values_list('book_id',flat=True))
		if book_list==[]:
			return Response()
		#按照list位置顺序进行排序
		queryset = Book.objects.filter(id__in=book_list).annotate(
			custom_sort=Case(
        *[When(id=value, then=pos) for pos, value in enumerate(book_list, start=1)],
        default=IntegerField()
    )
).order_by('custom_sort')

		page = self.paginate_queryset(queryset)
		if page is not None:
			serializer = BookListSerializer(page, many=True)
			return self.get_paginated_response(serializer.data)
		serializer = BookListSerializer(queryset, many=True)
		return Response(serializer.data)
		# queryset = self.filter_queryset(self.get_queryset())
		# page = self.paginate_queryset(queryset)
		# if page is not None:
		# 	serializer = self.get_serializer(page, many=True)
		# 	return self.get_paginated_response(serializer.data)
		#
		# serializer = self.get_serializer(queryset, many=True)
		# return Response(serializer.data)



