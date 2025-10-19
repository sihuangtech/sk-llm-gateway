# 百度（文心千帆）接入指南

本文档介绍如何获取百度文心千帆大模型的API Key和Secret Key，并配置到本系统中。

## 1. 访问官网

- **官方平台**：[百度智能云千帆大模型平台](https://cloud.baidu.com/product/wenxinworkshop)

## 2. 获取 API Key

1.  登录您的百度智能云账户。
2.  进入**千帆大模型平台**的控制台。
3.  在应用接入或类似菜单下，创建一个新应用，您将获得对应的 **API Key** 和 **Secret Key**。
4.  复制这两个值。

## 3. 配置到项目

将您复制的`API Key`和`Secret Key`粘贴到项目根目录下的 `.env` 文件中对应的`QIANFAN_AK`和`QIANFAN_SK`变量后。

```env
QIANFAN_AK=your_baidu_api_key_here
QIANFAN_SK=your_baidu_secret_key_here
```

**注意**：百度千帆的OpenAI兼容接口认证较为特殊，除了AK/SK，有时还需要通过它们定时获取`access_token`。本项目的`ModelManager`已做了简化处理，实际生产中可能需要根据官方文档实现token的自动刷新逻辑。

## 4. 可用模型参考

您可以在千帆大模型平台的模型广场中找到更多可用模型。以下是已在`models.yaml`中预置的模型：

- **语言模型**: `ERNIE-Speed-8K`
- **视觉模型**: `ERNIE-Vision-V4.0`

您可以通过Gradio管理后台动态添加其他模型。
