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
from django.core.cache import caches
from django.utils.deprecation import MiddlewareMixin

from blueapps.account.components.ptlogin.forms import AuthenticationForm
from blueapps.account.conf import ConfFixture
from blueapps.account.handlers.response import ResponseHandler

logger = logging.getLogger("component")
cache = caches["login_db"]


class LoginRequiredMiddleware(MiddlewareMixin):
    def process_view(self, request, view, args, kwargs):
        """
        可通过登录认证的方式，仅有两种
        1. 带有 login_exemp 标识的 view 函数
        2. 需要进行验证逻辑：
        # 先获得 cookie 并校验，失败进入 401 页面进行登录，其他情况继续执行
        # 在 session 和 cookie 中的 p_uin,p_skey 是否相同且用户有效
        直接 None 放行页面
        # 不满足上面的条件，则需要对 p_uin,p_skey 进行校验，并返回 user ，
        如果 user 对象存在，进行将 p_uin,p_skey 写入 session
        # 其他情况返回 401 页面 进行登录
        """
        if request.is_wechat():
            return None

        if hasattr(request, "is_bk_jwt") and request.is_bk_jwt():
            return None

        # 登录豁免
        if getattr(view, "login_exempt", False):
            return None

        user = self.authenticate(request)
        if user:
            return None

        # 验证不通过，需要跳转至统一登录平台
        handler = ResponseHandler(ConfFixture, settings)
        return handler.build_401_response(request)

    def process_response(self, request, response):
        return response

    def authenticate(self, request):
        form = AuthenticationForm(request.COOKIES)
        if not form.is_valid():
            return None
        uin = form.cleaned_data["p_uin"]
        skey = form.cleaned_data["p_skey"]
        session_key = request.session.session_key
        if session_key:
            cache_session = cache.get(session_key)
            # 确认 cookie 中的 uin sky 和 cache 中的是否一致
            is_match = (
                cache_session
                and uin == cache_session.get("p_uin")
                and skey == cache_session.get("p_skey")
            )
            if is_match and request.user.is_authenticated:
                return request.user
        user = auth.authenticate(request=request, uin=uin, skey=skey)
        if user and user.username != request.user.username:
            auth.login(request, user)
        if request.user.is_authenticated:
            # 登录成功，重新调用自身函数，即可退出
            cache.set(
                session_key,
                {"p_uin": uin, "p_skey": skey},
                settings.LOGIN_CACHE_EXPIRED,
            )
            return self.authenticate(request)
        return user
