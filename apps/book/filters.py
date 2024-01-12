import django_filters
from rest_framework import filters
from .models import Press, Book, BookType
from django.db.models import Q


# 自定义过滤器，根据url中的参数返回对应的内容
# 出版社过滤器
class PressFilter(django_filters.rest_framework.FilterSet):
	pressTitle = django_filters.CharFilter(field_name='pressTitle', lookup_expr='icontains')

	class Meta:
		model = Press
		fields = ['pressTitle', ]


# 书籍过滤器
class BookFilter(django_filters.rest_framework.FilterSet):
	search_key = django_filters.CharFilter(method="filter_search_key")
	press_id = django_filters.CharFilter()
	category = django_filters.CharFilter(method='fllter_category')

	@staticmethod
	def filter_search_key(queryset, name, value):
		return queryset.filter(Q(bookTitle__icontains=value) | Q(author__icontains=value))

	@staticmethod
	def fllter_category(queryset, name, value):
		category = BookType.objects.get(id=value)
		return category.category_books.filter(is_active=True)

	class Meta:
		model = Book
		fields = ['bookTitle', 'author', 'press_id', 'category']

# class BorrowFilter(django_filters.rest_framework.FilterSet):
# 	pressTitle = django_filters.CharFilter(field_name='pressTitle', lookup_expr='icontains')
#
# 	class Meta:
# 		model = Press
# 		fields = ['pressTitle', ]