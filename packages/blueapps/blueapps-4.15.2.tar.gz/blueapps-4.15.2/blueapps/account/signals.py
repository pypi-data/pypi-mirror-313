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
from django.contrib.auth import user_logged_out
from django.core.cache import caches
from django.dispatch import receiver


cache = caches["login_db"]


@receiver(user_logged_out)
def user_logged_out_handler(request, user, *args, **kwargs):
    session_key = request.session.session_key
    if session_key and cache.get(session_key):
        cache.delete(key=session_key)
