# CaiQiTalk LLM Service - API Documentation

本文档详细描述了 `backend-llm` 服务提供的所有API接口。所有接口都遵循OpenAI API格式规范，支持多种AI模型提供商。

## 基础信息

- **Base URL**: `http://localhost:8000`
- **认证**: 当前服务为内部服务，未设置认证。在生产环境中，应通过API网关进行保护。
- **Content-Type**: 
  - 对话接口: `application/json`
  - 视觉模型接口: `multipart/form-data`
- **响应格式**: 所有API响应均为JSON格式，除非特别说明（如流式响应）

---

## 1. AI 对话接口

### `POST /api/v1/chat/completions`

**描述**:
接收一个或多个消息组成的对话历史，与当前激活的语言大模型进行交互，并以流式（Server-Sent Events）的方式返回AI的回答。

**请求体 (Request Body)**:

- **Content-Type**: `application/json`

```json
{
  "messages": [
    {
      "role": "system",
      "content": "You are a helpful assistant."
    },
    {
      "role": "user",
      "content": "你好，请做个自我介绍。"
    }
  ],
  "stream": true
}
```

**参数说明**:
- `messages` (array, required): 对话消息列表，遵循OpenAI的格式。
  - `role` (string): 角色，可以是 `system`, `user`, 或 `assistant`。
  - `content` (string): 消息内容。
- `model` (string, optional): 指定使用的语言模型名称，如果不指定则使用当前激活的默认语言模型。
- `stream` (boolean, optional): 是否启用流式响应，默认为 `false`。

**响应 (Response)**:

- **Content-Type**: `application/json`（非流式）或 `text/event-stream`（流式）

**非流式响应**:
返回完整的AI回复内容：
```json
{
    "id": "chatcmpl-123456",
    "object": "chat.completion", 
    "created": 1234567890,
    "model": "gpt-3.5-turbo",
    "choices": [{
        "index": 0,
        "message": {
            "role": "assistant",
            "content": "这是一个Python快速排序的实现：..."
        },
        "finish_reason": "stop"
    }]
}
```

**流式响应**:
响应是一个事件流，每个事件块都包含部分文本内容。客户端需要持续接收并拼接这些文本块，以实现打字机效果。

**使用示例 (cURL)**:

```bash
# 非流式响应
curl -X POST "http://localhost:8000/api/v1/chat/completions" \
-H "Content-Type: application/json" \
-d '{
  "messages": [{"role": "user", "content": "用Python写一个快速排序"}],
  "stream": false
}'

# 流式响应
curl -N -X POST "http://localhost:8000/api/v1/chat/completions" \
-H "Content-Type: application/json" \
-d '{
  "messages": [{"role": "user", "content": "用Python写一个快速排序"}],
  "stream": true
}'
```

---

## 2. 视觉模型对话接口

### `POST /api/v1/vision/completions`

**描述**:
接收用户上传的图片，调用当前激活的视觉大模型进行分析，返回模型对图片内容的理解和分析结果。当前实现会询问图片中最主要的物体，并以结构化的格式返回识别结果。

**请求体 (Request Body)**:

- **Content-Type**: `multipart/form-data`

表单数据格式，包含图片文件和可选的模型参数。

**参数说明**:
- `image` (file, required): 需要分析的图片文件。
- `model` (string, optional): 指定使用的视觉模型名称，如果不指定则使用当前激活的默认视觉模型。

**响应 (Response)**:

- **Content-Type**: `application/json`

一个包含识别结果的JSON对象。当前实现会询问图片中最主要的物体，并返回结构化的识别信息。

```json
{
    "recognition_id": "chatcmpl-1234567890",
    "objects": [
        {
            "name": "猫",
            "description": "这是一只橘色的猫，它正坐在桌子上看着镜头。"
        }
    ]
}
```

**使用示例 (cURL)**:

```bash
# 将 'path/to/your/image.jpg' 替换为实际的图片路径
curl -X POST "http://localhost:8000/api/v1/vision/completions" \
-F "image=@path/to/your/image.jpg" \
-F "model=gpt-4-vision-preview"
```

---

## 3. 错误响应

当API调用失败时，服务会返回标准的HTTP错误状态码和错误信息：

```json
{
    "detail": "错误描述信息"
}
```

常见的错误状态码：
- `503 Service Unavailable`: 没有可用的模型服务
- `500 Internal Server Error`: 模型服务调用失败

---

## 4. 模型管理

### 4.1 获取可用模型列表

**端点 (Endpoint)**: `GET /api/v1/models`

**描述 (Description)**: 获取当前可用的AI模型列表。

**响应 (Response)**:

```json
{
    "object": "list",
    "data": [
        {
            "id": "gpt-3.5-turbo",
            "object": "model",
            "created": 1677610602,
            "owned_by": "openai"
        },
        {
            "id": "gpt-4-vision-preview", 
            "object": "model",
            "created": 1698894917,
            "owned_by": "openai"
        }
    ]
}
```

## 5. 管理后台

- **路径**: `/admin`
- **描述**: 一个基于Gradio的Web界面，用于管理和切换服务所使用的AI模型。详情请参考 `README.md`。

```