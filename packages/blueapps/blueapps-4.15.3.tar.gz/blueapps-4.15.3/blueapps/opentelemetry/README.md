# Blueapps OpenTelemetry 扩展使用说明

Blueapps OpenTelemetry 为开发者提供了开箱即用的蓝鲸 SaaS OpenTelemetry 接入工具，你可以通过他来实现

- Metric
  - 自动暴露 metrics server 并将指标采集到蓝鲸监控中
- Trace
  - 自动配置 OpenTelemetry SDK 与蓝鲸 SaaS 常用的 Instrumentor
  - 在本地通过 Jaeger 来收集 SaaS Trace 数据并进行可视化
  - 在线上通过蓝鲸日志平台来收集 SaaS Trace 数据并进行可视化
  - 将 OpenTelemetry TraceId SpanId 等相关信息集成到框架系统日志中，并在PaaS进行检索


## 使用说明

- [Trace](./docs/trace.md)
- [Metric](./docs/metric.md)