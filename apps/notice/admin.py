from django.contrib import admin
from simpleui.admin import AjaxAdmin
from .models import *
from django.conf import settings
import json
import os
import random
import time
import datetime
import string
# Register your models here.

@admin.register(Notice)
class NoticeAdmin(AjaxAdmin):
    list_display = ('id', 'title', 'notice_file', 'account','is_active','is_top')
    list_display_links = ['title']
    search_fields = ['title', 'content', 'account__username']
    fieldsets = (
		(None, {'fields': ( 'title', 'content', 'notice_file', 'account','is_active','is_top')}),
	)


