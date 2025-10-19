# 阿里云（通义千问）接入指南

本文档介绍如何获取阿里云通义千问大模型的API Key，并配置到本系统中。

## 1. 访问官网

- **官方平台**：[阿里云百炼大模型平台](https://www.aliyun.com/product/bailian)

## 2. 获取 API Key

1.  登录您的阿里云账户。
2.  进入**百炼大模型平台**的控制台。
3.  在左侧导航栏中找到“API Key管理”或类似入口。
4.  创建一个新的API Key。
5.  复制生成的API Key。

## 3. 配置到项目

将您复制的API Key粘贴到项目根目录下的 `.env` 文件中对应的`DASHSCOPE_API_KEY`变量后。

```env
DASHSCOPE_API_KEY=your_aliyun_api_key_here
```

## 4. 可用模型参考

您可以在阿里云百炼平台的模型广场中找到更多可用模型。以下是已在`models.yaml`中预置的模型：

- **语言模型**: `qwen-turbo`
- **视觉模型**: `qwen-vl-plus`

您可以通过Gradio管理后台动态添加其他模型。
