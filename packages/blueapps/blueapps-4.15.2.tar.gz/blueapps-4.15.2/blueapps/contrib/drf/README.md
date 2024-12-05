# Blueapps Django Rest Framework 扩展使用说明

Blueapps OpenTelemetry 为开发者提供了开箱即用的蓝鲸 SaaS OpenTelemetry 接入工具，你可以通过他来实现

Blueapp DRF 为开发者提供了常用的DRF工具类以及封装，帮助开发者快速构建REST风格的项目

提供的封装：
1. 统一异常处理: `blueapps.contrib.drf.exception.custom_exception_handler`
2. 统一接口返回: `blueapps.contrib.drf.renderers.APIRenderer`
3. ViewSet封装: `blueapps.contrib.drf.viewsets.APIViewSet`

提供的工具类：
1. 权限相关:
   1. 免除CSRF Token登录验证类: `blueapps.contrib.drf.utils.authentication.CsrfExemptSessionAuthentication`
2. Django Filter相关:
   1. 关键字过滤器: `blueapps.contrib.drf.utils.filters.GeneralSearchFilter`
   2. 排序过滤器: `blueapps.contrib.drf.utils.filters.GeneralOrderingFilter`
3. 分页类: `blueapps.contrib.drf.utils.pagination.CustomPageNumberPagination`
4. 序列化器字段相关:
   1. 整数列表Field: `blueapps.contrib.drf.utils.serializer_fields.MultipleIntField`
   2. 字符串列表Field: `blueapps.contrib.drf.utils.serializer_fields.MultipleStrField`
   3. 时间格式化Field: `blueapps.contrib.drf.utils.serializer_fields.CustomDateTimeField`
5. 序列化器相关:
   1. GeneralSerializer: 再封装ModelSerializer `blueapps.contrib.drf.utils.serializers.GeneralSerializer`
   2. 分页序列化器: `blueapps.contrib.drf.utils.serializers.PageSerializer`
   3. 排序序列化器: `blueapps.contrib.drf.utils.serializers.OrderingSerializer`
   4. 关键字搜索序列化器: `blueapps.contrib.drf.utils.serializers.SearchSerializer`
   5. ORM Condition查询序列化器: `blueapps.contrib.drf.utils.serializers.PostFilterSerializer`
6. 视图相关:
   1. DRF视图自定义校验器Mixin: `blueapps.contrib.drf.utils.viewset_mixin.ValidationMixin`


## Quick Start

### 0. 添加DRF配置

DRF相关配置已经集成于模版config/default.py中，如果是升级的项目，需要手动添加配置

### 1. 编写第一个DRF视图

使用提供的APIViewSet来编写视图类：
```python
from rest_framework.decorators import action
from rest_framework.response import Response

from blueapps.contrib.drf.viewsets import APIViewSet

class EntryViewSet(APIViewSet):
    """
    应用程序入口
    """

    @action(detail=False, methods=["get"], url_path="healthz")
    def healthz(self, request, *args, **kwargs):
        """
        获取应用健康状态
        """
        return Response({"healthy": True})

    @action(detail=False, methods=["get"], url_path="ping")
    def ping(self, request, *args, **kwargs):
        """
        应用ping 接口
        """
        return Response("pong")

```

### 2. 添加视图类Url

```python
from django.conf.urls import url
from django.urls import include
from rest_framework import routers

from . import views

router = routers.SimpleRouter()

router.register(r"", views.EntryViewSet, basename='healthz')

urlpatterns = (
    url(r"^entry/", include(router.urls)),
)
```


### 3. 访问/entry/healthz接口


## 扩展

如果提供的封装不符合要求，直接更改settings中的DRF配置即可