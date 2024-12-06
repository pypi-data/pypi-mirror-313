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
import socket
from django.conf import settings
from django_prometheus.middleware import (
    Metrics,
    PrometheusAfterMiddleware,
    PrometheusBeforeMiddleware,
)
from django_prometheus.utils import Time, TimeSince

HOSTNAME = socket.gethostname()
BK_ENV = os.getenv("BKPAAS_ENVIRONMENT", "dev")


class CustomMetrics(Metrics):
    def register_metric(self, metric_cls, name, documentation, labelnames=(), **kwargs):
        return super().register_metric(
            metric_cls, name, documentation, labelnames=[*labelnames, "hostname", "bk_env", "bk_app_code"], **kwargs
        )


class SaaSMetricsBeforeMiddleware(PrometheusBeforeMiddleware):
    metrics_cls = CustomMetrics

    def process_request(self, request):
        self.metrics.requests_total.labels(hostname=HOSTNAME, bk_env=BK_ENV, bk_app_code=settings.APP_CODE).inc()
        request.prometheus_before_middleware_event = Time()

    def process_response(self, request, response):
        self.metrics.responses_total.labels(hostname=HOSTNAME, bk_env=BK_ENV, bk_app_code=settings.APP_CODE).inc()
        if hasattr(request, "prometheus_before_middleware_event"):
            self.metrics.requests_latency_before.labels(
                hostname=HOSTNAME, bk_env=BK_ENV, bk_app_code=settings.APP_CODE
            ).observe(TimeSince(request.prometheus_before_middleware_event))
        else:
            self.metrics.requests_unknown_latency_before.labels(
                hostname=HOSTNAME, bk_env=BK_ENV, bk_app_code=settings.APP_CODE
            ).inc()
        return response


class SaaSMetricsAfterMiddleware(PrometheusAfterMiddleware):
    metrics_cls = CustomMetrics

    def label_metric(self, metric, request, response=None, **labels):
        labels.update({"hostname": HOSTNAME, "bk_env": BK_ENV, "bk_app_code": settings.APP_CODE})
        return super().label_metric(metric, request, response=response, **labels)
