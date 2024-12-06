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
import traceback

from django.conf import settings
from django.contrib.auth.backends import ModelBackend
from django.db import IntegrityError

from blueapps import metrics
from blueapps.account import get_user_model
from blueapps.account.conf import ConfFixture
from blueapps.account.utils.http import send
from blueapps.core.exceptions.base import MethodError
from blueapps.utils import client
from blueapps.utils.tools import resolve_login_url

logger = logging.getLogger("component")

ROLE_TYPE_ADMIN = "1"

TOKEN_TYPE = "bk_token"


class TokenBackend(ModelBackend):
    def authenticate(self, request=None, bk_token=None):
        logger.debug("Enter in TokenBackend")
        # 判断是否传入验证所需的bk_token,没传入则返回None
        if not bk_token:
            return None

        verify_result, username = self.verify_bk_token(bk_token, request)
        # 判断bk_token是否验证通过,不通过则返回None
        if not verify_result:
            return None

        user_model = get_user_model()
        try:
            user, _ = user_model.objects.get_or_create(username=username)
            get_user_info_result, user_info = self.get_user_info(bk_token)
            # 判断是否获取到用户信息,获取不到则返回None
            if not get_user_info_result:
                return None

            # 用户如果不是管理员，则需要判断是否存在平台权限，如果有则需要加上
            if not user.is_superuser and not user.is_staff:
                role = user_info.get("role", "")
                is_admin = True if str(role) == ROLE_TYPE_ADMIN else False
                user.is_superuser = is_admin
                user.is_staff = is_admin
                user.save()

            return user

        except IntegrityError:
            logger.exception(traceback.format_exc())
            logger.exception("get_or_create UserModel fail or update_or_create UserProperty")
            return None
        except Exception:  # pylint: disable=broad-except
            logger.exception(traceback.format_exc())
            logger.exception("Auto create & update UserModel fail")
            return None

    @staticmethod
    def get_user_info(bk_token):
        """
        请求平台ESB接口获取用户信息
        @param bk_token: bk_token
        @type bk_token: str
        @return:True, {
            u'message': u'\u7528\u6237\u4fe1\u606f\u83b7\u53d6\u6210\u529f',
            u'code': 0,
            u'data': {
                u'qq': u'',
                u'wx_userid': u'',
                u'language': u'zh-cn',
                u'username': u'test',
                u'time_zone': u'Asia/Shanghai',
                u'role': 2,
                u'phone': u'11111111111',
                u'email': u'test',
                u'chname': u'test'
            },
            u'result': True,
            u'request_id': u'eac0fee52ba24a47a335fd3fef75c099'
        }
        @rtype: bool,dict
        """
        api_params = {"bk_token": bk_token}

        try:
            response = client.bk_login.get_user(api_params)
        except Exception as err:  # pylint: disable=broad-except
            logger.exception("Abnormal error in get_user_info...:%s" % err)
            return False, {}

        if response.get("result") is True:
            # 由于v1,v2的get_user存在差异,在这里屏蔽字段的差异,返回字段相同的字典
            origin_user_info = response.get("data", "")
            user_info = dict()
            # v1,v2字段相同的部分
            user_info["wx_userid"] = origin_user_info.get("wx_userid", "")
            user_info["language"] = origin_user_info.get("language", "")
            user_info["time_zone"] = origin_user_info.get("time_zone", "")
            user_info["phone"] = origin_user_info.get("phone", "")
            user_info["chname"] = origin_user_info.get("chname", "")
            user_info["email"] = origin_user_info.get("email", "")
            user_info["qq"] = origin_user_info.get("qq", "")
            # v2版本特有的字段
            if settings.DEFAULT_BK_API_VER == "v2":
                user_info["username"] = origin_user_info.get("bk_username", "")
                user_info["role"] = origin_user_info.get("bk_role", "")
            # v1版本特有的字段
            elif settings.DEFAULT_BK_API_VER == "":
                user_info["username"] = origin_user_info.get("username", "")
                user_info["role"] = origin_user_info.get("role", "")
            return True, user_info
        else:
            error_msg = response.get("message", "")
            error_data = response.get("data", "")
            logger.error("Failed to Get User Info: error=%(err)s, ret=%(ret)s" % {"err": error_msg, "ret": error_data})
            return False, {}

    def verify_bk_token(self, bk_token, request=None):
        """
        请求VERIFY_URL,认证bk_token是否正确
        @param bk_token: "_FrcQiMNevOD05f8AY0tCynWmubZbWz86HslzmOqnhk"
        @type bk_token: str
        @return: False,None True,username
        @rtype: bool,None/str
        """
        try:
            return self.verify_bk_token_through_esb(bk_token)
        except (NotImplementedError, MethodError, AttributeError):
            # 对应版本 esb 不支持 client.bk_login.is_login 接口的情况
            return self.verify_bk_token_through_verify_url(bk_token, request)

    @staticmethod
    def verify_bk_token_through_esb(bk_token):
        api_params = {"bk_token": bk_token}

        try:
            with metrics.observe(
                metrics.BLUEAPPS_USER_TOKEN_VERIFY_DURATION,
                hostname=metrics.HOSTNAME,
                token_type=TOKEN_TYPE,
            ):
                response = client.bk_login.is_login(api_params)
        except (NotImplementedError, MethodError, AttributeError):
            raise
        except Exception:  # pylint: disable=broad-except
            metrics.BLUEAPPS_USER_TOKEN_VERIFY_FAILED_TOTAL.labels(
                hostname=metrics.HOSTNAME,
                token_type=TOKEN_TYPE,
                err="unknow_execption_raise",
            ).inc()
            logger.exception("Abnormal error in verify_bk_token...")
            return False, None

        if response.get("result"):
            data = response.get("data")
            username = data.get("bk_username")
            return True, username
        else:
            metrics.BLUEAPPS_USER_TOKEN_VERIFY_FAILED_TOTAL.labels(
                hostname=metrics.HOSTNAME, token_type=TOKEN_TYPE, err="verify_fail"
            ).inc()
            error_msg = response.get("message", "")
            error_data = response.get("data", "")
            logger.error("Fail to verify bk_token, error={}, ret={}".format(error_msg, error_data))
            return False, None

    @staticmethod
    def verify_bk_token_through_verify_url(bk_token, request=None):
        api_params = {"bk_token": bk_token}

        try:
            with metrics.observe(
                metrics.BLUEAPPS_USER_TOKEN_VERIFY_DURATION, hostname=metrics.HOSTNAME, token_type=TOKEN_TYPE
            ):
                response = send(
                    resolve_login_url(ConfFixture.VERIFY_URL, request, "http"),
                    "GET",
                    api_params,
                    verify=False,
                )
        except Exception:  # pylint: disable=broad-except
            metrics.BLUEAPPS_USER_TOKEN_VERIFY_FAILED_TOTAL.labels(
                hostname=metrics.HOSTNAME, token_type=TOKEN_TYPE, err="unknow_execption_raise"
            ).inc()
            logger.exception("Abnormal error in verify_bk_token...")
            return False, None

        if response.get("result"):
            data = response.get("data")
            username = data.get("username")
            return True, username
        else:
            metrics.BLUEAPPS_USER_TOKEN_VERIFY_FAILED_TOTAL.labels(
                hostname=metrics.HOSTNAME, token_type=TOKEN_TYPE, err="verify_fail"
            ).inc()
            error_msg = response.get("message", "")
            error_data = response.get("data", "")
            logger.error("Fail to verify bk_token, error={}, ret={}".format(error_msg, error_data))
            return False, None
