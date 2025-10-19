# 腾讯（混元）接入指南

本文档介绍如何获取腾讯混元大模型的`SecretId`和`SecretKey`，并配置到本系统中。

## 1. 访问官网

- **官方平台**：[腾讯云混元大模型](https://cloud.tencent.com/product/hunyuan)

## 2. 获取 API Key

1.  登录您的腾讯云账户。
2.  进入**访问管理 (CAM)** 控制台。
3.  在“API密钥管理”页面，可以查看或新建您的`SecretId`和`SecretKey`。
4.  请妥善保管这两个值，尤其是`SecretKey`，它只在创建时显示一次。

## 3. 配置到项目

将您获取的`SecretId`和`SecretKey`粘贴到项目根目录下的 `.env` 文件中对应的`HUNYUAN_SECRET_ID`和`HUNYUAN_SECRET_KEY`变量后。

```env
HUNYUAN_SECRET_ID=your_tencent_secret_id_here
HUNYUAN_SECRET_KEY=your_tencent_secret_key_here
```

**注意**：腾讯混元的认证机制较为复杂，通常需要使用SDK进行签名。本项目的`ModelManager`中对API Key的处理做了简化，实际生产环境中可能需要根据官方SDK实现更可靠的认证逻辑。

## 4. 可用模型参考

您可以在腾讯云官网查看混元大模型的具体版本和标识符。以下是已在`models.yaml`中预置的模型：

- **语言模型**: `hunyuan-pro`
- **视觉模型**: `hunyuan-vision`

您可以通过Gradio管理后台动态添加其他模型。
