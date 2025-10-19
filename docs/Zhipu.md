# 智谱AI (GLM) 接入指南

本文档介绍如何获取智谱AI大模型的API Key，并配置到本系统中。

## 1. 访问官网

- **官方平台**：[智谱AI开放平台](https://open.bigmodel.cn/)

## 2. 获取 API Key

1.  登录您的智谱AI账户。
2.  进入“API密钥”管理页面。
3.  创建一个新的API Key。
4.  复制生成的API Key。

## 3. 配置到项目

将您复制的API Key粘贴到项目根目录下的 `.env` 文件中对应的`ZHIPU_API_KEY`变量后。

```env
ZHIPU_API_KEY=your_zhipu_api_key_here
```

## 4. 可用模型参考

智谱AI的接口与OpenAI高度兼容，使用非常方便。以下是已在`models.yaml`中预置的模型：

- **语言模型**: `glm-4`
- **视觉模型**: `glm-4v`

您可以通过Gradio管理后台动态添加其他模型，如`glm-3-turbo`等。
