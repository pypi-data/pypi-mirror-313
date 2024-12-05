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

import time
import socket
from contextlib import contextmanager

try:
    from prometheus_client import Histogram, Counter
except ImportError:
    from unittest.mock import MagicMock
    Histogram = MagicMock()
    Counter = MagicMock()

HOSTNAME = socket.gethostname()

LATENCY_BUCKETS = (
    0.01,
    0.025,
    0.05,
    0.075,
    0.1,
    0.25,
    0.5,
    0.75,
    1.0,
    2.5,
    5.0,
    7.5,
    10.0,
    25.0,
    50.0,
    75.0,
    float("inf"),
)

BLUEAPPS_USER_TOKEN_VERIFY_DURATION = Histogram(
    name="blueapps_user_token_verify_duration",
    documentation="time spent verify user login token",
    buckets=LATENCY_BUCKETS,
    labelnames=["hostname", "token_type"],
)

BLUEAPPS_USER_TOKEN_VERIFY_FAILED_TOTAL = Counter(
    name="blueapps_user_token_verify_failed_total",
    documentation="Total count of user token verify failed",
    labelnames=["hostname", "token_type", "err"],
)


@contextmanager
def observe(histogram, **labels):
    start = time.time()
    yield
    histogram.labels(**labels).observe(time.time() - start)
