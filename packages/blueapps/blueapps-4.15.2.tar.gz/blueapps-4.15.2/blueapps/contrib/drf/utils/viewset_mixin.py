# -*- coding: utf-8 -*-
"""
Tencent is pleased to support the open source community by making 蓝鲸智云PaaS平台社区版 (BlueKing PaaS Community
Edition) available.
Copyright (C) 2017-2021 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License.
You may obtain a copy of the License at
http://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
"""
from rest_framework.authentication import BasicAuthentication, SessionAuthentication

from blueapps.contrib.drf.serializer import custom_params_valid
from blueapps.utils.logger import logger


class ApiMixin:
    """
    封装 APIViewSet 修改 ModelViewSet 默认返回内容，固定格式为
        {result: True, data: {}, code: 00, message: ''}
    """

    authentication_classes = (BasicAuthentication, SessionAuthentication)

    def initialize_request(self, request, *args, **kwargs):
        """
        Set the `.action` attribute on the view, depending on the request method.
        """
        logger.info(
            "[receive request], path: {}, header: {}, body: {}".format(
                request.path, request.headers.get("X-Bkapi-App"), request.body
            )
        )
        return super(ApiMixin, self).initialize_request(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        """
        `.dispatch()` is pretty much the same as Django's regular dispatch,
        but with extra hooks for startup, finalize, and exception handling.
        """
        return super().dispatch(request, *args, **kwargs)


class ValidationMixin:
    """
    DRF视图自定义校验器
    """

    def params_valid(self, serializer, params=None, instance=None, many=False, partial=False):
        """
        校验参数是否满足 serializer 规定的格式，支持传入serializer
        """
        # 校验request中的参数
        if not params:
            if self.request.method in ["GET"]:
                params = self.request.query_params
            else:
                params = self.request.data

        return custom_params_valid(serializer=serializer, params=params, instance=instance, many=many, partial=partial,)

    @property
    def validated_data(self):
        """
        校验的数据
        """
        # 优先使用缓存，避免多次取值时重复序列化和校验
        cache_validated_data = getattr(self, "cache_validated_data", None)
        if cache_validated_data:
            return cache_validated_data

        if self.request.method == "GET":
            data = self.request.query_params
        else:
            data = self.request.data
        serializer = self.serializer_class or self.get_serializer_class()
        cache_validated_data = self.params_valid(serializer, data)
        setattr(self, "cache_validated_data", cache_validated_data)
        return cache_validated_data
