# DeepSeek 接入指南

本文档介绍如何获取DeepSeek大模型的API Key，并配置到本系统中。

## 1. 访问官网

- **官方平台**：[DeepSeek开放平台](https://platform.deepseek.com/)

## 2. 获取 API Key

1.  登录您的DeepSeek账户。
2.  进入“API密钥”管理页面。
3.  创建一个新的API Key。
4.  复制生成的API Key。

## 3. 配置到项目

将您复制的API Key粘贴到项目根目录下的 `.env` 文件中对应的`DEEPSEEK_API_KEY`变量后。

```env
DEEPSEEK_API_KEY=your_deepseek_api_key_here
```

## 4. 可用模型参考

DeepSeek的接口与OpenAI高度兼容。以下是已在`models.yaml`中预置的模型：

- **语言模型**: `deepseek-chat`
- **视觉模型**: `deepseek-vl-chat`

您可以通过Gradio管理后台动态添加其他模型。
