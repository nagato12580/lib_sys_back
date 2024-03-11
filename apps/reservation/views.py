from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from apps.account.models import Account
from .serializers import ReservationSerializer,SeatSerializer
from .models import Reservation,Seat
from utils.common import Pagination
from .filters import SeatFilter
import copy
# Create your views here.
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
class SeatViewSet(ModelViewSet):
    '''社团公告视图'''
    queryset = Seat.objects.filter(is_active=True)
    serializer_class = SeatSerializer
    pagination_class = Pagination
    filter_class = SeatFilter
    filter_backends = (OrderingFilter, DjangoFilterBackend)
    ordering_fields = ('id', 'created_time','floor')

    @action(methods=['get'], detail=False, url_path='floor_seat')
    def floor_seat(self, request, *args, **kwargs):
        floor=request.GET.get('floor','')
        appointment_date=request.GET.get('appointment_date','')
        if not all([floor, appointment_date]):
            return Response({},status=status.HTTP_200_OK)
        else:
            #获取一楼所有座位列表
            seat_list=list(Seat.objects.filter(is_active=True,floor=floor).values('id','seat_number'))
            #复制一份，用于保存返回结果
            copy_data=copy.deepcopy(seat_list)
            # 指定要替换的键
            old_key_to_replace = 'seat_number'
            new_key = 'name'
            # 使用列表推导式和字典推导式替换键
            new_list_of_dicts = [{new_key if key == old_key_to_replace else key: value for key, value in d.items()} for d in copy_data]

            queryset=Reservation_set=Reservation.objects.select_related('seat').filter(is_active=True,
                                                       appointment_date=appointment_date,seat__floor=floor)\
            .values('seat', 'appointment_date','period')

            #grouped_data，键为seat_id,list为已被预约的时间列表
            grouped_data = {}
            for entry in queryset:
                seat_id = entry['seat']
                period = entry['period']
                if seat_id not in grouped_data:
                    grouped_data[seat_id] = []
                grouped_data[seat_id].append(period)



            for seat in seat_list:
                used_list=grouped_data.get(seat['id'],'')
                initial_array = [1] * 15
                if used_list:
                    for index in used_list:
                        initial_array[index]=0

                seat['usedList']=initial_array

            return Response({'floorListDetail':seat_list,'floorList':new_list_of_dicts},status=status.HTTP_200_OK)




class ReservationViewSet(ModelViewSet):
    '''社团公告视图'''
    queryset = Reservation.objects.filter(is_active=True)
    serializer_class = ReservationSerializer
    pagination_class = Pagination
    # filter_class = NoticeFilter
    filter_backends = (OrderingFilter, DjangoFilterBackend)
    ordering_fields = ('id', 'created_time')
    def create(self, request, *args, **kwargs):
        user_id=request.user.id
        seat_id = request.data.get('seat_id',[])
        time_list=request.data.get('time_list',[])
        appointment_date=request.data.get('appointment_date',[])
        for index in time_list:
            Reservation.objects.create(user_id=user_id,seat_id=seat_id,period=index,appointment_date=appointment_date)
        return Response(status=status.HTTP_200_OK)

