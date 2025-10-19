# Kimi / 月之暗面 (Moonshot) 接入指南

本文档介绍如何获取月之暗面（Kimi）大模型的API Key，并配置到本系统中。

## 1. 访问官网

- **官方平台**：[月之暗面开放平台](https://platform.moonshot.cn/)

## 2. 获取 API Key

1.  登录您的月之暗面账户。
2.  进入“API Key”管理页面。
3.  创建一个新的API Key。
4.  复制生成的API Key。

## 3. 配置到项目

将您复制的API Key粘贴到项目根目录下的 `.env` 文件中对应的`MOONSHOT_API_KEY`变量后。

```env
MOONSHOT_API_KEY=your_moonshot_api_key_here
```

## 4. 可用模型参考

月之暗面的接口与OpenAI高度兼容。以下是已在`models.yaml`中预置的模型：

- **语言模型**: `moonshot-v1-8k`

您也可以在Gradio后台添加其他版本的模型，如`moonshot-v1-32k`或`moonshot-v1-128k`。
