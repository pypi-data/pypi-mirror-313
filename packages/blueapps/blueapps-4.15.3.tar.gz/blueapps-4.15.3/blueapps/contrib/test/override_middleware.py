# -*- coding: utf-8 -*-
"""
Tencent is pleased to support the open source community by making 蓝鲸智云PaaS平台社区版 (BlueKing PaaS Community
Edition) available.
Copyright (C) 2017-2022 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License.
You may obtain a copy of the License at
http://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
"""
from django.utils.deprecation import MiddlewareMixin


class OverrideMiddleware(MiddlewareMixin):
    """
    用于跳过登录验证的中间件
    """

    def process_request(self, request):
        class Base(object):
            pass

        request.user = Base()
        request.source = "WEB"
        request.user.username = "admin"
        request.user.is_superuser = True
        request.user.is_authenticated = True
        request.user.is_active = True

        request.session = {"bluking_timezone": "Asia/Shanghai"}

        request.permission_exempt = True
        request.META.update({"HTTP_X_REQUESTED_WITH": "XMLHttpRequest"})
