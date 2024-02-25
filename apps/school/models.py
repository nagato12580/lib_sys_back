from django.db import models
from utils.common import BaseModel

# Create your models here.
class Faculty(BaseModel):
    name = models.CharField(verbose_name='学院名称', max_length=50)
    is_active = models.BooleanField(verbose_name='是否启用', default=True)

    class Meta:
        db_table = "faculty"
        verbose_name = "学院表"
        verbose_name_plural = verbose_name

class Major(BaseModel):
    name = models.CharField(verbose_name='专业名称', max_length=50)
    faculty = models.ForeignKey(Faculty, verbose_name='学院', related_name='major', on_delete=models.CASCADE)
    is_active = models.BooleanField(verbose_name='是否启用', default=True)

    class Meta:
        db_table = "major"
        verbose_name = "专业表"
        verbose_name_plural = verbose_name



