from django.contrib import admin
from .models import *
# Register your models here.
@admin.register(BookMessageTheme)
class BookMessageThemeAdmin(admin.ModelAdmin):
	list_display = ('id', 'book', 'title', 'user',  'is_active')
	list_display_links = ['title']
	search_fields = ['book__bookTitle', 'title', 'user__username']
	fieldsets = (
		(None, {'fields': ('book', 'title', 'user', 'content', 'is_active')}),
	)


@admin.register(MpttComment)
class MpttCommentAdmin(admin.ModelAdmin):
	list_display = ('id', 'theme', 'comment_user', 'comment_content', 'is_active')
	list_display_links = ['comment_content']
	search_fields = ['message__title', 'comment_content', 'comment_user__username']
	fieldsets = (
		(None, {'fields': ('message', 'comment_content', 'comment_user',  'is_active')}),
	)
	@admin.display(description='theme')
	def theme(self,obj):
		return obj.message.title


