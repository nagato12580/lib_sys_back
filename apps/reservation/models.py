from django.db import models
from apps.account.models import Account
from utils.common import BaseModel
lib_floor = {
    0: '负一楼',
    1: '一楼',
    2: '二楼',
    3: '三楼',
    4: '四楼',
    4: '五楼'
}
reservation_period = {
    0: "8:00-9:00",
    1: "9:00-10:00",
    2:"10:00-11:00",
    3:"11:00-12:00",
    4:"12:00-13:00",
    5:"13:00-14:00",
    6:"14:00-15:00",
    7:"15:00-16:00",
    8:"16:00-17:00",
    9:"17:00-18:00",
    10:"18:00-19:00",
    11:"19:00-20:00",
    12:"20:00-21:00",
    13:"21:00-22:00",
    14:"22:00-23:00",

}
class Seat(BaseModel):
    seat_number = models.CharField(verbose_name='座位编号', max_length=20)
    floor = models.PositiveIntegerField(verbose_name='楼层（数据字典中的lib_floor,0表负一楼，以此类推）', default=1)
    is_active = models.BooleanField(verbose_name='是否启用', default=True)
    class Meta:
        db_table = "seat"
        verbose_name = "座位表"
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.seat_number

class Reservation(BaseModel):
    seat = models.ForeignKey(Seat, verbose_name='预约座位', related_name='seat_reservation',
                             on_delete=models.CASCADE)
    user = models.ForeignKey(Account, verbose_name='预约人', related_name='account_reservation',
                             on_delete=models.CASCADE)
    is_active = models.BooleanField(verbose_name='是否启用', default=True)
    period = models.PositiveIntegerField(verbose_name='时间段（数据字典中的reservation_period，数值为当前小时-8）')
    appointment_date = models.DateField(verbose_name='预约日期')
    use_time = models.DateTimeField( verbose_name='使用时间', null=True)
    use_time = models.DateTimeField(verbose_name='使用时间', null=True)
    class Meta:
        db_table = "reservation"
        verbose_name = "座位预约表"
        verbose_name_plural = verbose_name