from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ('id', 'seat_number', 'floor', 'is_active')
    list_display_links = ['seat_number']
    search_fields = ['seat_number', 'floor']
    fieldsets = (
		(None, {'fields': ('seat_number', 'floor', 'is_active')}),
	)
@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('id', 'seat_number', 'user', 'period','appointment_date')
    list_display_links = ['seat_number']
    search_fields = ['seat__seat_number', 'floor','user__username']
    fieldsets = (
		(None, {'fields': ( 'seat', 'user', 'period','appointment_date')}),
	)

    @admin.display(description='seat_number')
    def seat_number(self, obj):
        return obj.seat.seat_number