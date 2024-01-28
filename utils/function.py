import json
import os
import random
import time
import datetime

from django.conf import settings
from django.http import JsonResponse
from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet



class UploadViewSet(GenericViewSet, mixins.CreateModelMixin):
    #上传轮播图接口
    @action(methods=['post'], detail=False, url_path='file')
    def upload(self, request, *args, **kwargs):
        file = request.data.get('file', None)
        dir_name = request.data.get('dir_name', '')
        if not all([file, dir_name]):
            return Response({'message': '缺少参数'}, status=status.HTTP_400_BAD_REQUEST)
        dir_path = f"{settings.MEDIA_ROOT}/lib_system/{dir_name}"
        if not os.path.exists(dir_path):  # 没有该目录就创建
            os.makedirs(dir_path)
        # 给文件重新命名，避免重复
        now_str = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        # name, suffix = os.path.splitext(image.name)
        # new_filename = now_str + name + suffix
        file_name = file.name
        new_filename = f"{random.randint(100, 999)}-{now_str}-{file_name}"
        img_path = os.path.join(dir_path, new_filename)
        # 写入文件
        with open(img_path, 'ab') as fp:
            # 如果上传的文件非常大，就通过chunks()方法分割成多个片段来上传
            for chunk in file.chunks():
                fp.write(chunk)
        img_path = f'lib_system/{dir_name}/{new_filename}'
        data = {
            'url': f'{settings.IMAGE_URL}{img_path}',
            'alt': new_filename,
        }
        result = {'errno': 0, 'data': data}
        return JsonResponse(result)

    #上传多个图片时使用，返回相对地址
    @action(methods=['post'], detail=False, url_path='upload_file')
    def upload_img(self, request, pk=None):
        """ 上传图片/文件 """
        file = request.data.get('file', None)
        dir_name = request.data.get('dir_name', '')
        if not all([file, dir_name]):
            return Response({'message': '缺少参数'}, status=status.HTTP_400_BAD_REQUEST)
        file_name = file.name
        dir_path = f"{settings.MEDIA_ROOT}/lib_system/{dir_name}"
        if not os.path.exists(dir_path):  # 没有该目录就创建
            os.makedirs(dir_path)
        # 给文件重新命名，避免重复
        now_str = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        new_file_name = f"{random.randint(100, 999)}-{now_str}-{file_name}"
        img_path = os.path.join(dir_path, new_file_name)
        # 写入文件
        with open(img_path, 'ab') as fp:
            # 如果上传的文件非常大，就通过chunks()方法分割成多个片段来上传
            for chunk in file.chunks():
                fp.write(chunk)
        img_path = f'lib_system/{dir_name}/{new_file_name}'
        return Response({'data': img_path, 'file_name': new_file_name})
