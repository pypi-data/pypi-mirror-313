# AWE (AI Workflow Engine)

AWE 是一个 AI 工作流引擎,用于对接 ComfyUI 并提供工作流调度能力。

## 功能特性

- 支持通过 RocketMQ 接收任务请求
- 支持调用 ComfyUI API 执行工作流
- 支持工作流模板和参数配置
- 支持进度、错误、完成事件通知
- 支持中英文提示词翻译
- 支持图片上传和结果处理

## 安装

```bash
pip install malette-awe
```

## 环境变量配置

需要配置以下环境变量:

```bash
# ComfyUI 配置
COMFYUI_HOST=localhost
COMFYUI_PORT=8188
# RocketMQ 配置
ROCKETMQ_ENDPOINT=xxx
ROCKETMQ_ACCESS_KEY=xxx
ROCKETMQ_ACCESS_SECRET=xxx
ROCKETMQ_INSTANCE_ID=xxx
ROCKETMQ_BASE_REQUEST_TOPIC=xxx
ROCKETMQ_BASE_RESPONSE_TOPIC=xxx
ROCKETMQ_BASE_GROUP_ID=xxx
ROCKETMQ_MESSAGE_TAG=xxx
ROCKETMQ_STATIC_TOPIC=false
ROCKETMQ_STATIC_GROUP=false
# 通义千问配置(用于中英文翻译)
DASHSCOPE_API_KEY=xxx
# 应用配置
ENV=dev
APPNAME=your_app_name
```

## 使用示例

```python
from awe import AWE

# 初始化 AWE
awe = AWE(
  comfyui_host="localhost",
  comfyui_port="8188"
)
# 启动服务
awe.start()
```

## 运行测试

安装测试依赖:

```bash
pip install -e ".[test]"
```

运行测试:

```bash
pytest tests/
```

运行测试覆盖率报告:

```bash
pytest --cov=src tests/
```
