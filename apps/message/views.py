from django.shortcuts import render
from rest_framework import viewsets, mixins
from utils.common import Pagination
from .models import BookMessageTheme,Comment,MpttComment
from .serializers import BookMessageThemeSerializer,CommentSerializer,MpttCommentListSerializer,MpttCommentDetailSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from utils.filters import BookMessageThemeFilter,CommentFilter,MpttCommentFilter
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView


# Create your views here.
#图书留言主题视图
class BookMessageThemeViewSet(viewsets.ModelViewSet):
	queryset = BookMessageTheme.objects.filter(is_active=True)
	serializer_class = BookMessageThemeSerializer
	pagination_class = Pagination
	filter_class = BookMessageThemeFilter
	filter_backends = (OrderingFilter, DjangoFilterBackend)

class CommentViewSet(viewsets.ModelViewSet):
	queryset = Comment.objects.filter(is_active=True)
	serializer_class = CommentSerializer
	pagination_class = Pagination
	filter_class = CommentFilter
	filter_backends = (OrderingFilter, DjangoFilterBackend)

	def list(self, request, *args, **kwargs):
		#过滤出该主题下面的回复
		queryset = Comment.objects.filter(is_active=True,pre_comment_id=None)
		page = self.paginate_queryset(queryset)
		if page is not None:
			serializer = self.get_serializer(page, many=True)
			return self.get_paginated_response(serializer.data)

		serializer = self.get_serializer(queryset, many=True)
		return Response(serializer.data)


class MpttCommentViewSet(viewsets.ModelViewSet):
	queryset = MpttComment.objects.filter(is_active=True)
	serializer_class = MpttCommentDetailSerializer
	pagination_class = Pagination
	filter_class = MpttCommentFilter
	filter_backends = (OrderingFilter, DjangoFilterBackend)

	# def get_serializer_class(self):
	# 	if self.action =='list':
	# 		return MpttCommentListSerializer
	# 	else:
	# 		return MpttCommentDetailSerializer

	#一级回复接口，即主题下的回复
	def create(self, request, *args, **kwargs):
		# message_id=request.data.get('message_id','')
		# comment_content = request.data.get('comment_content', '')
		# pre_comment_id = request.data.get('pre_comment_id', '')
		# reply_to_id = request.data.get('reply_to_id', '')
		# user_id=request.user.id
		# MpttComment.objects.create(message_id=message_id,comment_content=comment_content,comment_user_id=user_id)
		message_id=request.data.get('message_id','')
		comment_content = request.data.get('comment_content', '')
		parent_id = request.data.get('parent_id', '')
		reply_to_id = request.data.get('reply_to_id', '')
		user_id=request.user.id
		#二级以上的回复
		if parent_id:
		# 若回复层级超过二级，则转换为二级
		#找到父级评论
			parent_comment = MpttComment.objects.get(id=parent_id)
			#找到父级评论的根评论(即parent_id为空的一级评论)，转换为二级评论
			new_parent_id = parent_comment.get_root().id
			instance=MpttComment.objects.create(message_id=message_id, comment_content=comment_content,
									   comment_user_id=user_id,parent_id=new_parent_id,reply_to_id=reply_to_id)
		else:
			instance=MpttComment.objects.create(message_id=message_id, comment_content=comment_content,
									   comment_user_id=user_id,reply_to_id=reply_to_id)


		res={
			'id':instance.id,
			'parent_id':instance.parent_id,
			'comment_content':instance.comment_content,
			'reply_toto_id':instance.reply_to_id,
			'created_time':instance.created_time.strftime('%Y-%m-%d %H:%M'),
			'updated_time': instance.updated_time.strftime('%Y-%m-%d %H:%M')

		}
		return Response({'data':res}, status=status.HTTP_201_CREATED)



	# 二级回复接口，即对回复进行回复,废弃
	@action(methods=['post'], detail=False, url_path='seconde_reply')
	def seconde_reply(self, request, *args, **kwargs):
		message_id=request.data.get('message_id','')
		comment_content = request.data.get('comment_content', '')
		parent_id = request.data.get('parent_id', '')
		reply_to_id = request.data.get('reply_to_id', '')
		user_id=request.user.id
		if not all([message_id, comment_content,parent_id,reply_to_id,user_id]):
			return Response({'data':'缺少参数'}, status=status.HTTP_400_BAD_REQUEST)
		# 若回复层级超过二级，则转换为二级
		#找到父级评论
		parent_comment = MpttComment.objects.get(id=parent_id)
		#找到父级评论的根评论(即parent_id为空的一级评论)，转换为二级评论
		new_parent_id = parent_comment.get_root().id
		instance=MpttComment.objects.create(message_id=message_id, comment_content=comment_content,
								   comment_user_id=user_id,parent_id=new_parent_id,reply_to_id=reply_to_id)

		res={
			'id':instance.id,
			'parent_id':instance.parent_id,
			'comment_content':instance.comment_content,
			'reply_toto_id':instance.reply_to_id,
			'created_time':instance.created_time.strftime('%Y-%m-%d %H:%M'),
			'updated_time': instance.updated_time.strftime('%Y-%m-%d %H:%M')

		}
		return Response({'data':res}, status=status.HTTP_201_CREATED)

	def list(self, request, *args, **kwargs):
		data = MpttComment.objects.order_by('-created_time').filter(is_active=True,parent_id=None,reply_to_id=None)
		queryset = self.filter_queryset(data)

		page = self.paginate_queryset(queryset)
		if page is not None:
			serializer = self.get_serializer(page, many=True)
			return self.get_paginated_response(serializer.data)

		serializer = self.get_serializer(queryset, many=True)
		return Response(serializer.data)
