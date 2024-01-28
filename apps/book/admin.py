from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Book)
admin.site.register(BookRootType)
admin.site.register(BookType)
admin.site.register(Press)
admin.site.register(Borrow)
