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
from datetime import datetime
from collections import defaultdict
import copy
from django.db.models import Count
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

    @action(methods=['get'], detail=False, url_path='floor_overview')
    def floor_overview(self, request, *args, **kwargs):
        # 获取当前各楼座位使用情况
        hour=request.GET.get('hour')
        date=request.GET.get('date')
        index=int(hour)-8
        res=[100,100,100,100,100,100]
        #获取各层座位总数
        seat_counts = list(Seat.objects.filter(is_active=True).values('floor').annotate(count=Count('floor')))
        #获取各层座位使用数
        used_counts=list(Reservation.objects.select_related('seat').filter(is_active=True,period=index,appointment_date=date).values('seat__floor').annotate(count=Count('seat__floor')))
        for item in seat_counts:
            for used_item in used_counts:
                if(item['floor']==used_item['seat__floor']):
                    res[item['floor']]=100-int((used_item['count']/item['count'])*100)
        return Response({'res': res}, status=status.HTTP_200_OK)




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
        #查询预约日期当天该座位以被预约的时间段id
        used_seat_period=list(Reservation.objects.filter(is_active=True,seat_id=seat_id,appointment_date=appointment_date).values_list('period',flat=True))
        #获得两个列表的交集
        intersection = list(set(time_list) & set(used_seat_period))
        if intersection!=[]:
            #构造出冲突的时间
            res=[]
            for item in intersection:
                res.append(reservation_period.get(item))
            return Response(status=status.HTTP_400_BAD_REQUEST,data=res)
        for index in time_list:
            Reservation.objects.create(user_id=user_id,seat_id=seat_id,period=index,appointment_date=appointment_date)
        return Response(status=status.HTTP_200_OK)
    @action(methods=['get'], detail=False, url_path='my_reservation')
    def my_reservation(self, request, *args, **kwargs):

        user=request.user
        appointment_date=request.GET.get('appointment_date','')
        if not all([user]):
            return Response({'message':'未登录'}, status=status.HTTP_400_BAD_REQUEST)
        #获取未使用的座位列表
        #获取分组
        data=list(Reservation.objects.select_related('seat').filter(user=user,is_active=True,use_time__isnull=True).order_by('period','-appointment_date').values('seat_id','seat__seat_number','seat__floor','period','appointment_date'))
        # 使用 defaultdict 来按照 'appointment_date' 和 'seat_id' 进行分组
        grouped_data = defaultdict(lambda: defaultdict(list))
        for entry in data:
            grouped_data[entry['appointment_date']][entry['seat_id']].append(entry['period'])
        # 将分组后的数据转换为所需的格式
        formatted_data = []
        for appointment_date, appointments in grouped_data.items():
            for seat_id, periods in appointments.items():
                formatted_periods = [reservation_period[period] for period in periods]
                formatted_floor = lib_floor[data[0]['seat__floor']]  # 转换楼层信息
                entry = {
                    'appointment_date': appointment_date,
                    'seat_id': seat_id,
                    'floor': formatted_floor,  # 假设地板信息在所有数据中是相同的，可以根据实际情况修改
                    'seat_number': Seat.objects.get(id=seat_id).seat_number,  # 同上
                    'period': formatted_periods,
                }
                formatted_data.append(entry)
        return Response({'no_used_seat':formatted_data},status=status.HTTP_200_OK)

    @action(methods=['post'], detail=False, url_path='cancel_reservation')
    def cancel_reservation(self, request, *args, **kwargs):
        user=request.user
        seat_id=request.data.get('seat_id','')
        period_ids=request.data.get('period_ids',[])
        appointment_date=request.data.get('appointment_date','')
        if not all([user, appointment_date,seat_id,period_ids]):
            return Response({'message':'参数错误'}, status=status.HTTP_400_BAD_REQUEST)
        #更新
        try:
            instance = Reservation.objects.filter(user=user,seat_id=seat_id,period__in=period_ids,appointment_date=appointment_date,is_active=True).update(is_active=False)
        except Reservation.DoesNotExist:
            return Response({'message': '错误的参数'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message':'取消成功'},status=status.HTTP_200_OK)

    @action(methods=['post'], detail=False, url_path='use_reservation')
    def use_reservation(self, request, *args, **kwargs):
        user=request.user
        seat_id=request.data.get('seat_id','')
        period_id=request.data.get('period_id','')
        appointment_date=request.data.get('appointment_date','')
        if not all([user, appointment_date,seat_id,period_id]):
            return Response({'message':'参数错误'}, status=status.HTTP_400_BAD_REQUEST)
        # 获取当前日期和时间
        current_datetime = datetime.now()
        #更新
        try:
            instance = Reservation.objects.get(user=user,seat_id=seat_id,period=period_id,appointment_date=appointment_date,is_active=True,use_time__isnull=True)
        except Reservation.DoesNotExist:
            return Response({'message': '错误的参数'}, status=status.HTTP_400_BAD_REQUEST)
        instance.use_time=current_datetime
        instance.save()
        return Response({'message':'操作成功'},status=status.HTTP_200_OK)




