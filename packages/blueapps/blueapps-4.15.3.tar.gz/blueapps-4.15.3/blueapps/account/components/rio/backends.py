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

import hashlib
import logging
import time

from django.conf import settings
from django.contrib.auth.backends import ModelBackend
from django.utils.translation import gettext_lazy as _

from blueapps import metrics
from blueapps.account import get_user_model

logger = logging.getLogger("component")

TOKEN_TYPE = "rio"


class RioBackend(ModelBackend):
    def authenticate(
        self,
        request=None,
        timestamp=None,
        signature=None,
        staff_id=None,
        staff_name=None,
        x_ext_data=None,
        x_rio_seq=None,
    ):
        logger.debug("进入 RIO 认证 Backend")

        try:
            verify_data = self.verify_rio_request(
                request,
                timestamp=timestamp,
                signature=signature,
                staff_id=staff_id,
                staff_name=staff_name,
                x_ext_data=x_ext_data,
                x_rio_seq=x_rio_seq,
            )
        except UnicodeEncodeError as error:
            metrics.BLUEAPPS_USER_TOKEN_VERIFY_FAILED_TOTAL.labels(
                hostname=metrics.HOSTNAME, token_type=TOKEN_TYPE, err="rio_encode_error"
            ).inc()
            logger.exception("[RIO]编码异常: %s" % error)
            return None
        except Exception as err:
            metrics.BLUEAPPS_USER_TOKEN_VERIFY_FAILED_TOTAL.labels(
                hostname=metrics.HOSTNAME, token_type=TOKEN_TYPE, err="unknow_execption_raise"
            ).inc()
            logger.exception("[RIO]校验异常: %s" % err)
            return None

        logger.debug("RIO 验证结果，verify_data：%s" % verify_data)

        if not verify_data["result"] or not verify_data["data"]:
            return None

        user_info = verify_data["data"]
        user_model = get_user_model()
        try:
            user, _ = user_model.objects.get_or_create(username=user_info["username"])
            user.nickname = user_info["username"]
            user.save()
        except Exception as err:  # pylint: disable=broad-except
            logger.exception("自动创建 & 更新 User Model 失败: %s" % err)
            return None

        return user

    def get_user(self, user_id):
        user_model = get_user_model()
        try:
            return user_model.objects.get(pk=user_id)
        except user_model.DoesNotExist:
            return None

    @staticmethod
    def verify_rio_request(request, timestamp, signature, staff_id, staff_name, x_ext_data, x_rio_seq):
        """
        验证 RIO请求
        @param {string} timestamp 当前Unix时间戳，精确到秒，用于判断当前签名的时效性
        @param {string} signature 当前请求的签名(大写英文)，用于判断当前请求的合法
        @param {string} staff_id 员工的id
        @param {string} staff_name 员工的英文名
        @param {string} x_ext_data 微信的请求该字段为用户的 OpenID
        @param {string} x_rio_seq 当前请求的唯一的标识
        @return {dict} ret[1] 当 result=True，该字段为用户信息，举例
            {
                u'username': u'',
                u'avatar': u''
            }
        """
        ret = {"result": False, "message": "", "data": {}}

        if not timestamp or not signature:
            metrics.BLUEAPPS_USER_TOKEN_VERIFY_FAILED_TOTAL.labels(
                hostname=metrics.HOSTNAME, token_type=TOKEN_TYPE, err="param_loss"
            ).inc()
            logger.error("[RIO] login exception, param loss")
            ret["message"] = _("[RIO]login exception")
            return ret

        now = int(time.time())
        if abs(now - int(timestamp)) > 180:
            metrics.BLUEAPPS_USER_TOKEN_VERIFY_FAILED_TOTAL.labels(
                hostname=metrics.HOSTNAME, token_type=TOKEN_TYPE, err="rio_expired"
            ).inc()
            logger.error("[RIO] login time expire")
            ret["message"] = _("[RIO]login time expire")
            return ret

        token = getattr(settings, "RIO_TOKEN")

        # 校验
        with metrics.observe(
            metrics.BLUEAPPS_USER_TOKEN_VERIFY_DURATION, hostname=metrics.HOSTNAME, token_type=TOKEN_TYPE
        ):
            plaintext = timestamp + token + x_rio_seq + "," + staff_id + "," + staff_name + "," + x_ext_data + timestamp

            sign = hashlib.sha256(plaintext.encode()).hexdigest()

            if signature.lower() != sign.lower():
                logger.error("[RIO] login signature error {} vs {}".format(sign, signature))
                ret["message"] = _("[RIO]login signature error")
                return ret

        # 通过TOF获取用户信息
        # staff_info = get_staff_info_by_login_name(staffname)
        # if not staff_info:
        #    logger.error(u"[RIO]通过TOF获取用户信息异常")
        #    return result, data
        ret["result"] = True
        ret["data"] = {
            "username": staff_name,
        }
        return ret
