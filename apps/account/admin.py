from django.contrib import admin

# Register your models here.
from django.contrib import admin

# Register your models here.
from django.contrib import admin

from .models import Account

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
	list_display = ('id', 'username', 'is_staff', 'is_active', 'can_login_system', 'photo')
	list_display_links = ['username']
	search_fields = ['username', ]
	fieldsets = (
		(None, {'fields': ('username', 'password', 'is_superuser',
						   'is_staff', 'is_active', 'can_login_system', 'photo')}),
	)

	def save_model(self, request, obj, form, change):
		# 不是修改(则是新建)，或者修改了密码，则密码加密后保存
		if (not change) or (change and 'password' in form.changed_data):
			obj.set_password(obj.password)
		obj.save()





