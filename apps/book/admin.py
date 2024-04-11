from django.contrib import admin
from .models import *
from django.conf import settings
# Register your models here.


@admin.register(Press)
class PressAdmin(admin.ModelAdmin):
	list_display = ('id', 'pressTitle', 'contactPerson', 'telephone', 'email', 'is_active')
	list_display_links = ['pressTitle']
	search_fields = ['pressTitle', ]
	fieldsets = (
		(None, {'fields': ( 'pressTitle', 'contactPerson', 'telephone', 'email', 'is_active')}),
	)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
	list_display = ('id', 'ISBN', 'image_url', 'bookTitle', 'author', 'stockNumber','bookLocation','is_active')
	list_display_links = ['ISBN','bookTitle']
	search_fields = ['bookTitle', 'ISBN']
	fieldsets = (
		(None, {'fields': ('ISBN', 'image', 'bookTitle', 'author', 'stockNumber','bookLocation','is_active')}),
	)

	#添加新的列，展示图书封面
	@admin.display(description='image_url')
	def image_url(self,obj):
		return '{}{}'.format(settings.IMAGE_URL, obj.image)

@admin.register(BookType)
class BookTypeAdmin(admin.ModelAdmin):
	list_display = ('id', 'name', 'root_type', 'is_active')
	list_display_links = ['name']
	search_fields = ['name']
	fieldsets = (
		(None, {'fields': ( 'name', 'root_type', 'is_active')}),
	)

@admin.register(BookRootType)
class BookRootTypeAdmin(admin.ModelAdmin):
	list_display = ('id', 'name', 'is_active')
	list_display_links = ['name']
	search_fields = ['name']
	fieldsets = (
		(None, {'fields': ( 'name', 'is_active')}),
	)

@admin.register(Borrow)
class BorrowAdmin(admin.ModelAdmin):
	list_display = ('id', 'user', 'book','borrowing_date','is_return','return_data','total_return_data')
	list_display_links = ['user', 'book']
	search_fields = ['name','book','borrowing_date']
	fieldsets = (
		(None, {'fields': ( 'user', 'book','is_return','return_data','total_return_data')}),
	)