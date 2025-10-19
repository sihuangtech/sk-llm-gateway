# 字节跳动（火山引擎/豆包）接入指南

本文档介绍如何获取字节跳动火山引擎大模型的`Access Key ID`和`Secret Access Key`，并配置到本系统中。

## 1. 访问官网

- **官方平台**：[火山引擎大模型服务](https://www.volcengine.com/product/maas)

## 2. 获取 API Key

1.  登录您的火山引擎账户。
2.  进入**访问控制 (IAM)** 控制台。
3.  在“密钥管理”部分，创建或查看您的`Access Key ID (AK)`和`Secret Access Key (SK)`。
4.  复制这两个值。

## 3. 配置到项目

将您复制的AK和SK粘贴到项目根目录下的 `.env` 文件中对应的`VOLCANO_AK`和`VOLCANO_SK`变量后。

```env
VOLCANO_AK=your_volcano_ak_here
VOLCANO_SK=your_volcano_sk_here
```

**注意**：与百度、腾讯类似，火山引擎的认证也较为复杂。本项目的`ModelManager`中对API Key的处理做了简化，实际生产环境中可能需要根据官方SDK实现更可靠的认证逻辑。

## 4. 可用模型参考

您可以在火山引擎的模型广场中找到豆包系列模型的具体标识符。以下是已在`models.yaml`中预置的模型：

- **语言模型**: `Doubao-pro-8k`
- **视觉模型**: `Doubao-vision-pro`

您可以通过Gradio管理后台动态添加其他模型。
