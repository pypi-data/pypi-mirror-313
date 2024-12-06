## Quick Start

### 0. 安装扩展

```bash
pip install blueapps[opentelemetry]
```

### 1. 修改 Django 配置

在 `settings.INSTALLED_APPS` 中加入 `blueapps.opentelemetry.instrument_app`

```python
INSTALLED_APPS += (
    ...
    "blueapps.opentelemetry.instrument_app",
)

ENABLE_OTEL_TRACE = True

BK_APP_OTEL_INSTRUMENT_DB_API = True

# 日志中TRACE信息：可自定义格式，非必填，以默认值为例
OTEL_LOGGING_TRACE_FORMAT = "[trace_id]: %(otelTraceID)s [span_id]: %(otelSpanID)s [resource.service.name]: %(otelServiceName)s"
```

### 2. 启动 Jaeger

```bash
docker run -p 16686:16686 -p 6831:6831/udp jaegertracing/all-in-one
```

### 3. 启动进程

```bash
BKAPP_OTEL_SERVICE_NAME="server" python manage.py runserver --noreload 
BKAPP_OTEL_SERVICE_NAME="worker" celery worker -A blueapps.core.celery -P threads -c 300 -l info
```

### 4. 查看 trace 结果

访问 SaaS 任意页面后，访问 `http://localhost:16686/` 可查看上报的 trace 数据：

![](./docs/assets/local_jaeger.png)

## 可配置项

### 本地环境

- 环境变量
    - BKAPP_OTEL_SERVICE_NAME: 服务名，用于标识数据来源服务
- Django Settings
    - BKAPP_OTEL_SERVICE_NAME: 服务名，用于标识数据来源服务，**优先级低于环境变量**
    - ENABLE_OTEL_TRACE: 是否开启 trace
    - BK_APP_OTEL_INSTRUMENT_DB_API(`bool`): 是否开启 DB 访问 trace（开启后 span 数量会明显增多）
    - BK_APP_OTEL_ADDTIONAL_INSTRUMENTORS(`Collection[opentelemetry.instrumentation.instrumentor.BaseInstrumentor]`): 额外需要开启的 instrumentor，默认包含以下 instrumentor
        - LoggingInstrumentor
        - RequestsInstrumentor
        - DjangoInstrumentor
        - CeleryInstrumentor
        - RedisInstrumentor

### 线上环境

- 环境变量
    - BKAPP_OTEL_SERVICE_NAME: 服务名，用于标识数据来源服务，如果不配置，则默认使用 SaaS APP_CODE
    - BKAPP_OTEL_BK_DATA_ID: 日志平台数据上报 data id
    - BKAPP_OTEL_BK_DATA_TOKEN: 蓝鲸APM数据上报 data token
    - BKAPP_OTEL_GRPC_HOST: 日志平台数据上报 grpc host
    - BKAPP_OTEL_SAMPLER: 采样策略（always_on, always_off, parentbased_always_on, parentbased_always_off, traceidratio, parentbased_traceidratio），默认为 parentbased_always_off
- Django Settings
    - ENABLE_OTEL_TRACE: 是否开启 trace
    - BKAPP_OTEL_SERVICE_NAME: 服务名，用于标识数据来源服务，如果不配置，则默认使用 SaaS APP_CODE，**优先级低于环境变量**
    - BKAPP_OTEL_BK_DATA_ID: 日志平台数据上报 data id，**优先级低于环境变量**
    - BKAPP_OTEL_BK_DATA_TOKEN: 蓝鲸APM数据上报 data token，**优先级低于环境变量**
    - BKAPP_OTEL_GRPC_HOST: 日志平台数据上报 grpc host，**优先级低于环境变量**
    - BKAPP_OTEL_SAMPLER: 采样策略（always_on, always_off, parentbased_always_on, parentbased_always_off, traceidratio, parentbased_traceidratio），默认为 parentbased_always_off，**优先级低于环境变量**
    - BK_APP_OTEL_INSTRUMENT_DB_API(`bool`): 是否开启 DB 访问 trace（开启后 span 数量会明显增多）
    - BK_APP_OTEL_ADDTIONAL_INSTRUMENTORS(`Collection[opentelemetry.instrumentation.instrumentor.BaseInstrumentor]`): 额外需要开启的 instrumentor，默认包含以下 instrumentor
        - LoggingInstrumentor
        - RequestsInstrumentor
        - DjangoInstrumentor
        - CeleryInstrumentor
        - RedisInstrumentor
