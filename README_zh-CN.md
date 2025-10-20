# 彩旗工作室大模型统一管理平台

<div align="center">
  
  [English](./README.md) | [简体中文](./README_zh-CN.md)
  
</div>

一个支持多厂商、多模型的大语言模型统一管理平台。该平台基于FastAPI构建，提供统一的API接口和Gradio管理后台，支持动态管理和切换各种AI模型。

## ✨ 功能特性

- **统一API接口**：为多种AI功能（如对话、视觉）提供统一的API端点。
- **多模型支持**：通过配置文件 `config/models.yaml` 支持并预置了多家主流AI服务商（智谱、月之暗面、阿里、百度、腾讯、字节）以及Ollama本地部署的模型。
- **OpenAI兼容**：使用标准的OpenAI SDK进行调用，切换模型厂商只需更改配置，无需修改代码。
- **动态管理后台**：内置Gradio Web UI，允许管理员：
  - 实时切换当前服务所使用的语言和视觉模型。
  - 动态添加新的模型配置到系统中。
  - **模型测试功能**：支持在管理后台直接测试语言模型和视觉模型，包括：
    - 语言模型测试：可自定义测试消息，实时查看模型响应
    - 视觉模型测试：支持图片上传和图文混合测试，自动处理图片格式转换
- **现代化工具链**：使用 `uv` 和 `pyproject.toml` 进行项目和依赖管理。
- **流式响应**：支持Server-Sent Events流式响应，实现打字机效果。
- **视觉模型对话**：提供专门的视觉模型接口，支持图片上传和视觉分析功能。
- **模型测试功能**：在管理后台直接测试语言模型和视觉模型，包括：
  - 语言模型测试：可自定义测试消息，实时查看模型响应
  - 视觉模型测试：支持图片上传和图文混合测试，自动处理图片格式转换

## 🚀 技术栈

- **Web框架**: FastAPI
- **管理后台**: Gradio
- **AI模型调用**: OpenAI SDK
- **配置**: Pydantic, PyYAML
- **包管理**: uv
- **图像处理**: PIL (Pillow)
- **数据格式**: Base64, JSON
- **异步处理**: Python asyncio

## 📁 项目结构

```
backend-llm/
├── app/                    # 应用代码
│   ├── admin/             # Gradio管理后台
│   ├── api/               # API接口
│   │   └── v1/            # API版本1
│   ├── core/              # 核心功能
│   ├── schemas/           # 数据模型
│   └── services/          # 业务服务
├── config/                # 配置文件
│   ├── models.yaml        # 模型配置
│   └── providers/         # 供应商配置
├── docs/                  # 文档
├── main.py               # 应用入口
├── pyproject.toml        # 项目配置
└── requirements.txt      # 依赖列表
```

## ⚙️ 配置说明

在启动服务之前，您需要配置API密钥和平台信息。

1.  **复制配置文件**：将项目根目录下的 `.env.example` 文件复制一份，并重命名为 `.env`。

    ```bash
    cp .env.example .env
    ```

2.  **配置平台名称**（可选）：在 `.env` 文件中设置您的平台名称，默认为"大模型统一管理平台"。

    ```env
    PLATFORM_NAME=大模型统一管理平台
    ```

3.  **填入API密钥**：打开 `.env` 文件，将您从各模型供应商处获取的API密钥填入对应的环境变量中。例如：

    ```env
    ZHIPU_API_KEY=your_zhipu_api_key_here
    MOONSHOT_API_KEY=your_moonshot_api_key_here
    # ... 其他模型的密钥
    ```

## 🚀 快速开始

### 1. 安装UV（超快Python包管理器）

UV是一个比pip快10-100倍的现代Python包管理器和虚拟环境管理工具。

#### 安装UV（跨平台）

**macOS/Linux:**
```bash
# 使用官方安装脚本
curl -LsSf https://astral.sh/uv/install.sh | sh

# 或者使用Homebrew（macOS）
brew install uv
```

**Windows:**
```powershell
# 使用官方安装脚本
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# 使用winget安装UV
winget install --id=astral-sh.uv  -e

# 使用Scoop安装UV
scoop install main/uv
```

**验证安装:**
```bash
uv --version
# 输出类似: uv 0.4.x
```

#### UV基本使用

**创建项目虚拟环境:**
```bash
# 在项目目录下创建虚拟环境
uv venv

# 激活虚拟环境
# macOS/Linux:
source .venv/bin/activate
# Windows:
.venv\Scripts\activate
```

**安装依赖:**
```bash
# 从pyproject.toml安装所有依赖
uv pip install -e .

# 或者使用uv run直接运行（推荐，无需手动激活环境）
uv run uvicorn main:app --reload
```

### 2. 项目设置

```bash
# 克隆项目并进入目录（如果尚未克隆）
cd sk-llm-gatewat

# 使用UV创建虚拟环境（可选，uv run会自动处理）
uv venv
```

### 3. 配置环境

```bash
# 复制环境配置文件
cp .env.example .env

# 编辑.env文件，填入您的API密钥
nano .env  # 或使用您喜欢的编辑器
```

### 4. 启动服务

```bash
# 使用uv直接运行（推荐 - 无需手动激活虚拟环境）
uv run uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# 或者先激活虚拟环境再运行
source .venv/bin/activate  # macOS/Linux
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 5. 访问服务

- **管理后台**: http://localhost:8000/admin
- **API文档**: http://localhost:8000/docs
- **API文档**: http://localhost:8000/redoc

### 6. 测试功能

1. 访问管理后台，点击"模型测试"选项卡
2. 测试语言模型：输入消息并查看响应
3. 测试视觉模型：上传图片并输入描述

## 📦 详细安装步骤

如果您需要更详细的安装步骤，请参考以下说明：

### 虚拟环境（可选）

如果您希望手动创建虚拟环境：

1.  **创建虚拟环境**：

    ```bash
    # 在项目根目录下运行
    uv venv
    ```

2.  **激活虚拟环境**：

    ```bash
    # Windows
    .venv\Scripts\activate

    # macOS / Linux
    source .venv/bin/activate
    ```

3.  **安装依赖**：

    ```bash
    # uv 会自动从 pyproject.toml 安装依赖
    uv pip install -e .
    ```

### 启动服务

```bash
uv run uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

使用 `uv run` 的好处是无需手动激活虚拟环境，uv会自动管理运行环境。

## 🕹️ 使用说明

服务启动后：

- **API 服务**: 运行在 `http://localhost:8000`。所有API端点都在此基地址下。
- **管理后台**: 通过浏览器访问 `http://localhost:8000/admin` 即可进入Gradio管理界面。

在管理后台，您可以：
- **模型管理**: 方便地切换当前激活的模型，或添加新的模型配置
- **模型测试**: 在"模型测试"选项卡中测试语言和视觉模型：
  - **语言模型测试**: 输入自定义消息或直接测试，查看模型响应效果
  - **视觉模型测试**: 上传图片并输入描述，进行图文混合测试

### API接口说明

服务提供以下API接口：
- **对话接口**: `POST /api/v1/chat/completions` - 支持流式响应的AI对话
- **视觉模型对话接口**: `POST /api/v1/vision/completions` - 图片上传和视觉分析
- **管理后台**: `/admin` - Gradio管理界面

详细的API文档请参考 [API_DOCS.md](API_DOCS.md) 文件。

## 🎬 功能演示

### 模型管理功能

服务启动后，访问 `http://localhost:8000/admin`，您可以使用以下功能：

#### 模型切换与管理
- 在管理界面中，可以方便地切换当前激活的语言模型和视觉模型
- 支持动态添加新的模型配置到系统中
- 实时查看模型状态和配置信息

#### 模型测试功能
- **语言模型测试**：在"模型测试"选项卡左侧，可以输入自定义测试消息，实时查看模型响应效果
- **视觉模型测试**：在"模型测试"选项卡右侧，支持图片上传和图文混合测试
  - 可以上传图片并输入描述，进行完整的视觉理解测试
  - 图片上传后会自动转换为base64格式，支持常见的图片格式

### API使用示例

#### 对话API示例
```bash
curl -N -X POST "http://localhost:8000/api/v1/chat/completions" \
-H "Content-Type: application/json" \
-d '{
  "messages": [{"role": "user", "content": "用Python写一个快速排序"}],
  "stream": true
}'
```

#### 视觉模型对话API示例
```bash
curl -X POST "http://localhost:8000/api/v1/vision/completions" \
-F "image=@path/to/your/image.jpg" \
-F "model=gpt-4-vision-preview"
```

## 🚀 部署选项 (Deployment Options)

### 开发环境 (Development)

在开发阶段，推荐使用`uv`和`uvicorn`直接启动服务，因为它支持代码热重载，非常方便调试。

```bash
# 使用uv运行，无需手动激活虚拟环境
uv run uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 生产环境 (Production)

在生产环境中，不推荐直接使用`uvicorn`命令，而应使用更健壮的进程管理器。

#### 选项1: Gunicorn + Uvicorn (推荐)

这是部署Python ASGI应用（如FastAPI）的黄金组合。Gunicorn作为进程管理器，负责启动和管理多个Uvicorn工作进程，可以更好地利用服务器多核资源，并保证服务的稳定性。

1.  **额外安装gunicorn**:
    ```bash
    uv pip install gunicorn
    ```

2.  **使用gunicorn启动服务**:
    ```bash
    # 启动4个Uvicorn工作进程
    gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app -b 0.0.0.0:8000
    ```
    - `-w 4`: 指定工作进程的数量，通常建议为 `(2 * CPU核心数) + 1`。
    - `-k uvicorn.workers.UvicornWorker`: 告诉Gunicorn使用Uvicorn的工作进程类来处理请求。
    - `-b 0.0.0.0:8000`: 绑定服务的地址和端口。

#### 选项2: Docker 容器化部署

将整个应用打包成Docker镜像是在现代云环境中部署的标准方式。以下是一个示例`Dockerfile`：

```Dockerfile
# 使用官方Python基础镜像
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 安装uv
RUN pip install uv

# 复制配置文件和依赖定义文件
COPY pyproject.toml ./

# 使用uv安装依赖
# --system 表示安装到系统python环境中，因为容器内是隔离的
RUN uv pip install --system -e .

# 复制所有应用代码
COPY . .

# 暴露端口
EXPOSE 8000

# 容器启动命令 (使用Gunicorn)
CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "main:app", "-b", "0.0.0.0:8000"]
```

使用此`Dockerfile`，您就可以构建一个包含所有依赖和代码的镜像，并轻松地将其部署到任何支持Docker的平台（如Docker Swarm, Kubernetes, 或云服务商的容器服务）。

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件。

## 📞 社区支持

如果您有任何问题或需要帮助，欢迎加入我们的社区：

[![Discord](https://img.shields.io/badge/Discord-加入我们的Discord服务器-7289da?logo=discord&logoColor=white)](https://discord.gg/thWGWq7CwA)
[![QQ群](https://img.shields.io/badge/QQ群-加入我们的QQ群-12b7f5?logo=qq&logoColor=white)](https://qm.qq.com/q/WEBm0AkBKI)

## ⭐ 星标历史

[![Star History Chart](https://api.star-history.com/svg?repos=sihuangtech/sk-llm-gateway&type=date&legend=top-left)](https://www.star-history.com/#sihuangtech/sk-llm-gateway&type=date&legend=top-left)
