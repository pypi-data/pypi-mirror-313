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

from django.contrib.auth.backends import ModelBackend

from blueapps import metrics
from blueapps.account import get_user_model
from blueapps.account.conf import ConfFixture
from blueapps.account.utils.http import send
from blueapps.utils.tools import resolve_login_url

logger = logging.getLogger("component")

TOKEN_TYPE = "bk_ticket"


class TicketBackend(ModelBackend):
    def authenticate(self, request=None, bk_ticket=None):
        logger.debug("进入 Paas 认证 Backend")
        if not bk_ticket:
            return None

        result, user_info = self.verify_bk_ticket(bk_ticket, request)
        if not result:
            return None

        user_model = get_user_model()
        user, _ = user_model.objects.get_or_create(username=user_info["username"])
        user.nickname = user_info["username"]
        user.avatar_url = user_info["avatar_url"]
        user.save()
        return user

    @staticmethod
    def verify_bk_ticket(bk_ticket, request=None):
        """
        验证 OA 登录票据
        @param {string} bk_ticket OA 登录票据
        @return {tuple} ret
        @return {boolean} ret[0] 是否认证通过
        @return {dict} ret[1] 当 result=True，该字段为用户信息，举例
            {
                'username': 'tester',
                'avatar_url': 'http://???.??.com/avatars/tester/avatar.jpg'
            }
        """
        api_params = {"bk_ticket": bk_ticket}
        try:
            with metrics.observe(
                metrics.BLUEAPPS_USER_TOKEN_VERIFY_DURATION, hostname=metrics.HOSTNAME, token_type=TOKEN_TYPE
            ):
                response = send(
                    resolve_login_url(ConfFixture.USER_INFO_URL, request, "http"),
                    "GET",
                    api_params,
                )
            ret = response.get("ret")

            if ret == 0:
                return True, response["data"]
            else:
                metrics.BLUEAPPS_USER_TOKEN_VERIFY_FAILED_TOTAL.labels(
                    hostname=metrics.HOSTNAME, token_type=TOKEN_TYPE, err="verify_fail"
                ).inc()
                logger.error("bk_ticket 验证失败，error={}，ret={}".format(response["msg"], ret))
                return False, None
        except Exception:  # pylint: disable=broad-except
            metrics.BLUEAPPS_USER_TOKEN_VERIFY_FAILED_TOTAL.labels(
                hostname=metrics.HOSTNAME, token_type=TOKEN_TYPE, err="unknow_execption_raise"
            ).inc()
            logger.exception("bk_ticket 验证异常")
            return False, None
