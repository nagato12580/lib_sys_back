from .models import Reservation,Seat
import django_filters
from rest_framework import filters

class SeatFilter(django_filters.rest_framework.FilterSet):
	floor = django_filters.CharFilter(field_name='floor', lookup_expr='icontains')

	class Meta:
		model = Seat
		fields = ['floor', ]