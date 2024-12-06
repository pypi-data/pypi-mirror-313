# -*- coding: utf-8 -*-
"""
Tencent is pleased to support the open source community by making 蓝鲸智云PaaS平台社区版 (BlueKing PaaS Community
Edition) available.
Copyright (C) 2017-2022 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License.
You may obtain a copy of the License at
http://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
"""

import functools
import json

from django.core.cache import cache
from django.core.serializers.json import DjangoJSONEncoder

from blueapps.utils.base import md5_sum
from blueapps.utils.constants import TimeEnum
from blueapps.utils.logger import logger


def using_cache(key: str, duration, need_md5=False):
    """
    缓存方法返回值
    :param key: key 名可以使用format进行格式
    :param duration: 过期时间
    :param need_md5: 缓冲是redis的时候 key不能带有空格等字符，需要用md5 hash一下
    :return: function
    """

    def decorator(func):
        @functools.wraps(func)
        def inner(*args, **kwargs):

            try:
                actual_key = key.format(*args, **kwargs)
            except (IndexError, KeyError):
                actual_key = key

            logger.info(f"[using cache] build key => [{actual_key}] duration => [{duration}]")

            if need_md5:
                actual_key = md5_sum(actual_key)

            cache_result = cache.get(actual_key)

            if cache_result:
                return json.loads(cache_result)

            result = func(*args, **kwargs)
            if result:
                cache.set(actual_key, json.dumps(result, cls=DjangoJSONEncoder), duration)
            return result

        return inner

    return decorator


cache_half_minute = functools.partial(using_cache, duration=0.5 * TimeEnum.ONE_MINUTE_SECOND)
cache_one_minute = functools.partial(using_cache, duration=TimeEnum.ONE_MINUTE_SECOND)
cache_five_minute = functools.partial(using_cache, duration=5 * TimeEnum.ONE_MINUTE_SECOND)
cache_ten_minute = functools.partial(using_cache, duration=10 * TimeEnum.ONE_MINUTE_SECOND)
cache_one_hour = functools.partial(using_cache, duration=TimeEnum.ONE_HOUR_SECOND)
cache_one_day = functools.partial(using_cache, duration=TimeEnum.ONE_DAY_SECOND)
