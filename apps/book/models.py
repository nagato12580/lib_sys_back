from django.db import models

# Create your models here.

from django.db import models
# Create your models here.
from utils.common import BaseModel
from apps.account.models import Account


# 图书二级分类表格

class BookRootType(BaseModel):
	# ID:主键
	name = models.CharField(verbose_name='类别', max_length=10)
	is_active = models.BooleanField(verbose_name='假删除', default=True)

	class Meta:
		db_table = "book_root_type"
		verbose_name = "图书一级分类"
		verbose_name_plural = verbose_name

	def __str__(self):
		return self.name
class BookType(BaseModel):
	# ID:主键
	name = models.CharField(verbose_name='类别', max_length=10)
	is_active = models.BooleanField(verbose_name='假删除', default=True)
	root_type=models.ForeignKey(BookRootType, verbose_name='图书一级分类', related_name='second_type', on_delete=models.CASCADE)


	class Meta:
		db_table = "book_type"
		verbose_name = "图书二级分类"
		verbose_name_plural = verbose_name

	def __str__(self):
		return self.name


# 出版社
class Press(BaseModel):
	# ID:主键
	pressNo = models.CharField(verbose_name='出版社编号', max_length=12, unique=True, editable=False)
	pressTitle = models.CharField(verbose_name='出版社名称', max_length=40)
	address = models.CharField(verbose_name='出版社地址', max_length=40)
	zipCode = models.CharField(verbose_name='邮政编码', max_length=6)
	contactPerson = models.CharField(verbose_name='联系人', max_length=12)
	telephone = models.CharField(verbose_name='联系电话', max_length=15)
	email = models.EmailField(verbose_name='邮箱')  # 默认验证邮箱有效性
	is_active = models.BooleanField(verbose_name='假删除', default=True)

	class Meta:
		db_table = "press"
		verbose_name = "出版社"
		verbose_name_plural = verbose_name

	def __str__(self):
		return self.pressTitle


class Book(BaseModel):
	# ID:主键
	ISBN = models.CharField(verbose_name='书籍编号', max_length=17)
	image = models.CharField(verbose_name='图书封面', max_length=100)  # 改用String方式存储
	bookTitle = models.CharField(verbose_name='书名', max_length=30)
	author = models.CharField(verbose_name='作者', max_length=40)
	publishDate = models.DateField(verbose_name='出版日期')
	version = models.IntegerField(verbose_name='版次', null=True, blank=True)
	category = models.ManyToManyField(BookType, verbose_name='书籍分类', related_name='category_books')
	stockNumber = models.IntegerField(verbose_name='馆藏数量', default=0)
	checkedOutBooks = models.IntegerField(verbose_name='已借出图书数量', default=0)
	bookLocation = models.CharField(verbose_name='藏书地址', max_length=40)
	introduction = models.TextField(max_length=500, verbose_name='内容简介')
	is_active = models.BooleanField(default=True, verbose_name='假删除')
	press = models.ForeignKey(Press, verbose_name='出版社', related_name='books', on_delete=models.CASCADE)
	class Meta:
		db_table = "book"
		verbose_name = "图书"
		verbose_name_plural = verbose_name
		#联合唯一约束




	def __str__(self):
		return self.bookTitle



class Borrow(BaseModel):
	user= models.ForeignKey(Account, verbose_name='借阅人', related_name='books', on_delete=models.CASCADE)
	book=models.ForeignKey(Book,verbose_name='借阅图书', related_name='users', on_delete=models.CASCADE)
	is_return=models.BooleanField(default=False, verbose_name='是否归还')
	borrowing_date = models.DateField(verbose_name='借阅日期', auto_now_add = True) #第一次创建时设置日期
	return_data=models.DateField(verbose_name='预计归还日期',null=False,blank=False)
	total_return_data = models.DateField(verbose_name='实际归还日期',null=True,blank=True)
	class Meta:
		db_table = "borrow"
		verbose_name = "图书借阅"
		verbose_name_plural = verbose_name

class BookCollection(BaseModel):
	user = models.ForeignKey(Account, verbose_name='借阅人', related_name='star_book', on_delete=models.CASCADE)
	book = models.ForeignKey(Book, verbose_name='借阅图书', related_name='star_user', on_delete=models.CASCADE)
	is_active=models.BooleanField(default=True)
	class Meta:
		db_table = "collection"
		verbose_name = "图书收藏"
		verbose_name_plural = verbose_name