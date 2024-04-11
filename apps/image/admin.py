from django.contrib import admin
from .models import *
# Register your models here.
from django.conf import settings

@admin.register(LibSwiper)
#todo 待修改，编辑页面添加上传图片按钮
class LibSwiperAdmin(admin.ModelAdmin):
	list_display = ('id', 'image_1','image_2', 'image_3','is_active')
	list_display_links = ['id']
	fieldsets = (
		(None, {'fields': ('cover','is_active')}),
	)
	@admin.display(description='image_1')
	def image_1(self,obj):
		return '{}{}'.format(settings.IMAGE_URL, obj.cover[0]["data"])
	@admin.display(description='image_2')
	def image_2(self,obj):
		return '{}{}'.format(settings.IMAGE_URL, obj.cover[1]["data"])
	@admin.display(description='image_3')
	def image_3(self,obj):
		return '{}{}'.format(settings.IMAGE_URL, obj.cover[2]["data"])