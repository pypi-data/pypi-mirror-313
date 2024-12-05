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
    BACKEND_TYPE = "bk_ticket"
    USER_BACKEND = "bk_ticket.backends.TicketBackend"
    LOGIN_REQUIRED_MIDDLEWARE = "bk_ticket.middlewares.LoginRequiredMiddleware"
    USER_MODEL = "bk_ticket.models.UserProxy"

    LOGIN_URL = (os.getenv("BKPAAS_LOGIN_DOMAIN") or os.getenv("BKPAAS_LOGIN_URL", "")).strip("/") + "/"
    LOGIN_PLAIN_URL = f"{LOGIN_URL}plain/?size=full"
    USER_INFO_URL = f"{LOGIN_URL}user/get_info"
    USER_FULL_INFO_URL = f"{LOGIN_URL}user/get_full_info"
    ADD_CROSS_PREFIX = False
    ADD_APP_CODE = False

    IFRAME_HEIGHT = 490
    IFRAME_WIDTH = 900

    WEIXIN_BACKEND_TYPE = "weixin"
    WEIXIN_MIDDLEWARE = "weixin.middlewares.WeixinLoginRequiredMiddleware"
    WEIXIN_BACKEND = "weixin.backends.WeixinBackend"
    WEIXIN_INFO_URL = f"{LOGIN_URL}user/weixin/get_user_info/"
    WEIXIN_OAUTH_URL = os.environ.get(
        "BK_WEIXIN_OAUTH_URL", "https://open.weixin.qq.com/connect/oauth2/authorize"
    )
    WEIXIN_APP_ID = os.environ.get("BK_WEIXIN_APP_ID", "")

    SMS_CLIENT_MODULE = "smcs"
    SMS_CLIENT_FUNC = "send_sms_for_ieod"
    SMS_CLIENT_USER_ARGS_NAME = "receiver"
    SMS_CLIENT_CONTENT_ARGS_NAME = "message"

    RIO_BACKEND_TYPE = "rio"
    RIO_MIDDLEWARE = "rio.middlewares.RioLoginRequiredMiddleware"
    RIO_BACKEND = "rio.backends.RioBackend"

    BK_JWT_MIDDLEWARE = "bk_jwt.middlewares.BkJwtLoginRequiredMiddleware"
    BK_JWT_BACKEND = "bk_jwt.backends.BkJwtBackend"
