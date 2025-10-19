# Ollama (本地部署) 接入指南

本文档介绍如何配置Ollama，以供本系统在本地调用模型。

## 1. 安装与运行Ollama

- **官方网站**：[Ollama](https://ollama.com/)

1.  根据您的操作系统（macOS, Linux, Windows）从官网下载并安装Ollama。
2.  安装完成后，Ollama服务通常会自动在后台运行。

## 2. 拉取模型

打开您的终端，使用`ollama run`命令来下载并运行您需要的模型。例如：

- **拉取Llama 3语言模型**:
  ```bash
  ollama run llama3
  ```

- **拉取LLaVA视觉模型**:
  ```bash
  ollama run llava
  ```

Ollama会自动下载模型并启动交互。您可以随时关闭交互，模型已经存在于本地。

## 3. 配置到项目

Ollama默认在本机`11434`端口提供服务，并且通常不需要API Key。

1.  确保`config/models.yaml`文件中Ollama的`base_url`指向正确地址（默认为`http://localhost:11434/v1`）。
2.  `.env`文件中的`OLLAMA_API_KEY`可以保留默认的`ollama`或留空。

## 4. 可用模型参考

您可以在Ollama官网的[Models页面](https://ollama.com/library)查看所有可用的模型。以下是已在`models.yaml`中预置的模型：

- **语言模型**: `ollama-llama3` (对应Ollama中的`llama3`模型)
- **视觉模型**: `ollama-llava` (对应Ollama中的`llava`模型)

当您想使用Ollama中的其他模型时（例如`mistral`），建议在Gradio后台**动态添加新模型**，名称可以设为`ollama-mistral`，模型类型选择`language`，并填入正确的Base URL即可。
