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
from __future__ import unicode_literals

import logging

from django.conf import settings
from django.utils.encoding import force_str
from django.utils.translation import gettext_lazy as _


class BlueException(Exception):
    """
    异常统一封装类
    """

    PLATFORM_CODE = getattr(settings, "PLATFORM_CODE", "00")
    MODULE_CODE = "00"
    ERROR_CODE = "500"
    MESSAGE = _("APP异常")
    STATUS_CODE = 500
    LOG_LEVEL = logging.ERROR

    def __init__(self, *args, message=None, data=None, **kwargs):
        """
        :param message: 错误消息
        :param data: 其他数据
        :param context: 错误消息 format dict
        :param args: 其他参数
        """
        super(BlueException, self).__init__(*args)

        if len(self.ERROR_CODE) == 3:
            code = f"{self.PLATFORM_CODE}{self.MODULE_CODE}{self.ERROR_CODE}"
        else:
            # 兼容旧版ERROR_CODE异常码长度不为3位 -> 只组合平台码和异常码
            code = f"{self.PLATFORM_CODE}{self.ERROR_CODE}"

        self.code = code
        self.errors = kwargs.get("errors")
        # 优先使用第三方系统的错误编码
        if kwargs.get("code"):
            self.code = kwargs["code"]

        self.message = force_str(message) if message else force_str(self.MESSAGE)

        self.data = data

    def __str__(self):
        return "[{}] {}".format(self.code, self.message)

    def render_data(self):
        """
        返回异常信息
        """
        return self.data

    def response_data(self):
        """
        返回response数据
        """
        return {
            "result": False,
            "code": self.code,
            "message": self.message,
            "data": self.render_data(),
        }


class ClientBlueException(BlueException):
    """
    客户端请求异常
    """

    MESSAGE = _("客户端请求异常")
    ERROR_CODE = "400"
    STATUS_CODE = 400


class ServerBlueException(BlueException):
    """
    服务器异常
    """

    MESSAGE = _("服务端服务异常")
    ERROR_CODE = "500"
    STATUS_CODE = 500


class ResourceNotFound(ClientBlueException):
    """
    客户端异常：找不到请求的资源
    """

    MESSAGE = _("找不到请求的资源")
    ERROR_CODE = "404"
    STATUS_CODE = 404


class ParamValidationError(ClientBlueException):
    """
    客户端异常：参数验证失败
    """

    MESSAGE = _("参数验证失败")
    ERROR_CODE = "400"
    STATUS_CODE = 400


class ParamRequired(ClientBlueException):
    """
    客户端异常：关键参数缺失
    """

    MESSAGE = _("关键参数缺失")
    ERROR_CODE = "401"
    STATUS_CODE = 400


class AccessForbidden(ClientBlueException):
    """
    客户端异常：登陆失败
    """

    MESSAGE = _("登陆失败")
    ERROR_CODE = "413"
    STATUS_CODE = 403


class RequestForbidden(ClientBlueException):
    """
    客户端异常：请求拒绝
    """

    MESSAGE = _("请求拒绝")
    ERROR_CODE = "423"
    STATUS_CODE = 403


class ResourceLock(ClientBlueException):
    """
    客户端异常：请求资源被锁定
    """

    MESSAGE = _("请求资源被锁定")
    ERROR_CODE = "433"
    STATUS_CODE = 403


class MethodError(ClientBlueException):
    """
    客户端异常：请求方法不支持
    """

    MESSAGE = _("请求方法不支持")
    ERROR_CODE = "405"
    STATUS_CODE = 405


class RioVerifyError(ClientBlueException):
    """
    客户端异常：智能网关检测失败
    """

    MESSAGE = _("登陆请求经智能网关检测失败")
    ERROR_CODE = "415"
    STATUS_CODE = 405


class BkJwtVerifyError(ClientBlueException):
    """
    客户端异常：JWT检测失败
    """

    MESSAGE = _("登陆请求经JWT检测失败")
    ERROR_CODE = "425"
    STATUS_CODE = 401


class DatabaseError(ServerBlueException):
    """
    服务端异常：数据库异常
    """

    MESSAGE = _("数据库异常")
    ERROR_CODE = "501"


class ApiNetworkError(ServerBlueException):
    """
    服务端异常：网络异常
    """

    MESSAGE = _("网络异常导致远程服务失效")
    ERROR_CODE = "503"
    STATUS_CODE = 503


class ApiResultError(ServerBlueException):
    """
    服务端异常：远程服务请求结果异常
    """

    MESSAGE = _("远程服务请求结果异常")
    ERROR_CODE = "513"
    STATUS_CODE = 503


class ApiNotAcceptable(ServerBlueException):
    """
    服务端异常：远程服务返回结果格式异常
    """

    MESSAGE = _("远程服务返回结果格式异常")
    ERROR_CODE = "523"
    STATUS_CODE = 503


class LocalError(ServerBlueException):
    """
    服务端异常：组件调用异常
    """

    MESSAGE = _("组件调用异常")
    ERROR_CODE = "533"


class LockError(ServerBlueException):
    MESSAGE = _("获取锁失败")
    ERROR_CODE = "543"
