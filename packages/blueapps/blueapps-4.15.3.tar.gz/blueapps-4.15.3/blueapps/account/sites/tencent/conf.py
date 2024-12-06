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
import os


class ConfFixture(object):
    BACKEND_TYPE = "ptlogin"
    USER_BACKEND = "ptlogin.backends.PtloginBackend"
    LOGIN_REQUIRED_MIDDLEWARE = "ptlogin.middlewares.LoginRequiredMiddleware"
    USER_MODEL = "ptlogin.models.UserProxy"

    LOGIN_URL = (os.getenv("BKPAAS_LOGIN_DOMAIN") or os.getenv("BKPAAS_LOGIN_URL", "")).strip("/") + "/"
    LOGIN_PLAIN_URL = f"{LOGIN_URL}plain/"
    VERIFY_URL = f"{LOGIN_URL}user/is_login/"
    ADD_CROSS_PREFIX = False
    ADD_APP_CODE = True

    # 用于get_user_info的esb api调用的配置
    GET_USER_INFO_COLLECTION = "oidb"
    GET_USER_INFO_COLLECTION_API = "get_user_info_by_uin"
    GET_USER_INFO_COLLECTION_PARAMS = ("uin", "skey")

    IFRAME_HEIGHT = 390
    IFRAME_WIDTH = 670

    WEIXIN_BACKEND_TYPE = "null"
    WEIXIN_MIDDLEWARE = "null.NullMiddleware"
    WEIXIN_BACKEND = "null.NullBackend"

    SMS_CLIENT_MODULE = "cmsi"
    SMS_CLIENT_FUNC = "send_sms_for_external_user"
    SMS_CLIENT_USER_ARGS_NAME = "receiver__uin"
    SMS_CLIENT_CONTENT_ARGS_NAME = "content"

    RIO_BACKEND_TYPE = "null"
    RIO_MIDDLEWARE = "null.NullMiddleware"
    RIO_BACKEND = "null.NullBackend"

    BK_JWT_MIDDLEWARE = "bk_jwt.middlewares.BkJwtLoginRequiredMiddleware"
    BK_JWT_BACKEND = "bk_jwt.backends.BkJwtBackend"
