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

import logging

from django.conf import settings
from django.contrib import auth
from django.utils.deprecation import MiddlewareMixin

from blueapps.account.components.rio.forms import RioAuthenticationForm
from blueapps.account.conf import ConfFixture
from blueapps.account.handlers.response import ResponseHandler

logger = logging.getLogger("component")


class RioLoginRequiredMiddleware(MiddlewareMixin):
    def process_view(self, request, view, args, kwargs):
        """
        可通过登录认证的请求：
        1. 带有 RIO HTTP HEADER
        2. RIO签名正确
        """
        # 框架前置中间件，已将识别的客户端信息填充进 request
        if not hasattr(request, "is_rio") or not request.is_rio():
            return None

        logger.debug("当前请求是否经过RIO转发")
        login_exempt = getattr(view, "login_exempt", False)

        if login_exempt or request.user.is_authenticated:
            return None

        # 每次请求都需要做校验
        user = self.authenticate(request)
        if user:
            return None

        handler = ResponseHandler(ConfFixture, settings)
        return handler.build_rio_401_response(request)

    def process_response(self, request, response):
        return response

    def authenticate(self, request):
        form = RioAuthenticationForm(request.META)
        if not form.is_valid():
            logger.debug(
                u"[RIO]未检测到请求标识，url：{}，params：{}, errors: {}".format(
                    request.path_info, request.META, form.errors
                )
            )
            return None

        timestamp = form.cleaned_data["HTTP_TIMESTAMP"]
        signature = form.cleaned_data["HTTP_SIGNATURE"]
        staff_id = form.cleaned_data["HTTP_STAFFID"]
        staff_name = form.cleaned_data["HTTP_STAFFNAME"]
        x_ext_data = form.cleaned_data["HTTP_X_EXT_DATA"]
        x_rio_seq = form.cleaned_data["HTTP_X_RIO_SEQ"]
        logger.debug(u"RIO请求链接，检测到验证码：%s" % (signature))

        user = auth.authenticate(
            request=request,
            timestamp=timestamp,
            signature=signature,
            staff_id=staff_id,
            staff_name=staff_name,
            x_ext_data=x_ext_data,
            x_rio_seq=x_rio_seq,
        )
        if user and user.username != request.user.username:
            auth.login(request, user)
        if request.user.is_authenticated:
            # 登录成功，确认登陆正常后退出
            return request.user
        return user
