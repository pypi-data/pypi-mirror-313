## 最佳实践

- 开发框架 metrics 模块通过守护线程的方式对外暴露 metrics server endpoint，所以请在单个 pod 中使用单业务进程模型进行部署（即 gunicorn、celery 等进程使用单进程多线程/单进程多协程模型），并以 pod 为维度进行扩容。
- 如果一定要使用多进程模型，请使用自定义上报而非 metrics server 进行指标上报：[bk-monitor-report](https://github.com/TencentBlueKing/bk-monitor-report/)

## Quick Start

### 0. 升级框架版本

```bash
pip install blueapps[opentelemetry] >= 4.4.5
```

### 1. 安装 APP

确保 INSTALLED_APPS 中添加了如下应用：

```
INSTALLED_APPS += (
    ...
    "blueapps.opentelemetry.instrument_app",
)

ENABLE_OTEL_METRICS = True

```

### 2. 确认使用了正确的 wsgi 应用

请确保使用了由 `blueapps.core.wsgi.get_wsgi_application` 函数返回的 wsgi 应用

以下是 `wsgi.py` 文件的样例

```py
import os

from blueapps.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

application = get_wsgi_application()
```

### 3. 打破黑盒😎

等待片刻，即可在蓝鲸监控中的基本 SaaS 仪表盘中看到数据

## 如何暴露自定义指标

使用 [prometheus-client](https://github.com/prometheus/client_python) 进行指标定义和记录即可，所有定义的指标都会被采集到蓝鲸监控中。