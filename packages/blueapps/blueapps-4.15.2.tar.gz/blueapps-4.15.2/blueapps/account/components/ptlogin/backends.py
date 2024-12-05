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
from django.contrib.auth.backends import ModelBackend

from blueapps import metrics
from blueapps.account import get_user_model
from blueapps.account.conf import ConfFixture
from blueapps.account.utils.http import send
from blueapps.utils import client
from blueapps.utils.tools import resolve_login_url

logger = logging.getLogger("component")

TOKEN_TYPE = "uin_skey"


class PtloginBackend(ModelBackend):
    def authenticate(self, request=None, uin=None, skey=None):

        if uin and skey:
            result = self.verify_uin_skey(uin, skey, request)
            if not result:
                return None
        else:
            return None

        user_model = get_user_model()
        user, _ = user_model.objects.get_or_create(username=uin)
        user_info = self.get_user_info(request, uin, skey)
        if user_info is not None:
            user.nickname = user_info["nick_name"]
            user.avatar_url = user_info["avatar_url"]
            user.save()
        return user

    @staticmethod
    def get_user_info(request, uin, skey):
        api_params = {"uin": uin, "skey": skey}
        # 根据ConfFixture.GET_USER_INFO_COLLECTION配置项获取esb调用对象
        get_user_info_collection = getattr(client, ConfFixture.GET_USER_INFO_COLLECTION)
        # 根据ConfFixture.GET_USER_INFO_COLLECTION_API配置项获取esb调用对象的api函数
        get_user_info_api = getattr(get_user_info_collection, ConfFixture.GET_USER_INFO_COLLECTION_API)
        # 根据GET_USER_INFO_COLLECTION_KWARGS配置项构造esb调用对象的api函数需要的参数
        get_user_info_params = {_key: api_params[_key] for _key in ConfFixture.GET_USER_INFO_COLLECTION_PARAMS}
        # 调用esb
        response = get_user_info_api(get_user_info_params)
        if response["result"]:
            return response["data"]
        else:
            return None

    @staticmethod
    def verify_uin_skey(uin, skey, request=None):
        """
        验证登录票据的有效性
        """
        api_params = {"app_code": settings.APP_CODE, "skey": skey, "uin": uin}
        # noinspection PyBroadException
        try:
            with metrics.observe(
                metrics.BLUEAPPS_USER_TOKEN_VERIFY_DURATION, hostname=metrics.HOSTNAME, token_type=TOKEN_TYPE
            ):
                response = send(
                    resolve_login_url(ConfFixture.VERIFY_URL, request, "http"),
                    "GET",
                    api_params,
                )
            if not response["result"]:
                metrics.BLUEAPPS_USER_TOKEN_VERIFY_FAILED_TOTAL.labels(
                    hostname=metrics.HOSTNAME, token_type=TOKEN_TYPE, err="verify_fail"
                ).inc()
                logger.error("uin，skey 验证失败，error=%s" % response["message"])
                return False
            else:
                return True
        except Exception as err:  # pylint: disable=broad-except
            metrics.BLUEAPPS_USER_TOKEN_VERIFY_FAILED_TOTAL.labels(
                hostname=metrics.HOSTNAME, token_type=TOKEN_TYPE, err="unknow_execption_raise"
            ).inc()
            logger.exception("uin，skey 验证异常，error=%s" % err)
            return False
