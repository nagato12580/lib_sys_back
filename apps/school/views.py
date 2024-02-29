from django.shortcuts import render
from rest_framework import viewsets, mixins
from utils.common import Pagination
from .models import Faculty,Major
from .serializers import FacultySerializer,MajorSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

# Create your views here.



class FacultyViewSet(viewsets.ModelViewSet):
	queryset = Faculty.objects.filter(is_active=True)
	serializer_class = FacultySerializer
	pagination_class = Pagination

class MajorViewSet(viewsets.ModelViewSet):
	queryset = Major.objects.filter(is_active=True)
	serializer_class = MajorSerializer
	pagination_class = Pagination
	@action(methods=['get'], detail=False, url_path='get_facult_major')
	def get_book_second_category(self, request):
		faculty_id=request.GET.get('faculty_id')
		queryset = Major.objects.filter(faculty_id=faculty_id,is_active=True)
		serializer = MajorSerializer(queryset, many=True)
		return Response(serializer.data, status=status.HTTP_200_OK)

