from django.db import models
from utils.common import BaseModel

# Create your models here.
class LibSwiper(BaseModel):
    cover = models.JSONField(verbose_name='小程序首页轮播图')
    is_active = models.BooleanField(verbose_name='是否启用', default=True)

    class Meta:
        db_table = "lib_swiper"
        verbose_name = "小程序首页轮播图"
        verbose_name_plural = verbose_name

