from django.shortcuts import render
from rest_framework import viewsets, mixins
from utils.common import Pagination
from .models import Faculty

# Create your views here.



class FacultyViewSet(viewsets.ModelViewSet):
	queryset = Faculty.objects.filter(is_active=True)
	serializer_class = FacultySerializer
	pagination_class = Pagination

