# SK LLM Gateway

<div align="center">
  
  [English](./README.md) | [简体中文](./README_zh-CN.md)
  
</div>

A unified management platform for large language models, supporting multiple vendors and models with a unified API interface.

## ✨ Features

- 🚀 **Multi-vendor Support**: Unified access to OpenAI, Anthropic, Google, Alibaba, Baidu, Tencent, ByteDance, Zhipu, and more
- 🔄 **Model Switching**: Dynamically switch between different AI models
- 🎨 **Visual Models**: Support for GPT-4 Vision, Claude, and other visual understanding models
- 📊 **Management Dashboard**: Gradio-based web interface for easy model management
- 🔧 **Unified API**: Single API endpoint compatible with OpenAI format
- ⚡ **High Performance**: Built with FastAPI for optimal performance
- 🔐 **Secure**: API key management and secure configuration

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Client Apps   │    │  SK-LLM Gateway │    │  AI Providers   │
│                 │───▶│                 │───▶│   OpenAI        │
│  - Mobile Apps  │    │  - Unified API  │    │   Anthropic     │
│  - Web Apps     │    │  - Model Mgmt   │    │   Google        │
│  - Desktop Apps │    │  - Load Balance │    │   Alibaba       │
└─────────────────┘    └─────────────────┘    │   Baidu         │
                                              │   ...           │
                                              └─────────────────┘
```

## 🚀 Quick Start

### 1. Install UV

**macOS/Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows:**
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 2. Project Setup

```bash
# Enter project directory
cd backend-llm

# Run with UV (auto handles virtual environment)
uv run uvicorn main:app --reload
```

### 3. Configure Environment

```bash
# Copy environment config file
cp .env.example .env

# Edit .env file, add your API keys
nano .env
```

### 4. Start Service

```bash
# Run with UV (auto handles virtual environment)
uv run uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 5. Access Services

- **Management Dashboard**: http://localhost:8000/admin
- **API Documentation**: http://localhost:8000/docs
- **Alternative API Docs**: http://localhost:8000/redoc

### 6. Test Features

1. Visit management dashboard, click "Model Testing" tab
2. Test language models: Enter messages and view responses
3. Test visual models: Upload images and enter descriptions

## 📦 Supported Providers

### Language Models
- **OpenAI**: GPT-4, GPT-3.5, etc.
- **Anthropic**: Claude 3, Claude 2
- **Google**: Gemini Pro, Gemini Vision
- **Alibaba**: Tongyi Qianwen
- **Baidu**: ERNIE Bot
- **Tencent**: Hunyuan
- **ByteDance**: Skylark
- **Zhipu**: GLM-4
- **DeepSeek**: DeepSeek Chat

### Visual Models
- **OpenAI**: GPT-4 Vision
- **Anthropic**: Claude 3 Vision
- **Google**: Gemini Pro Vision
- **Zhipu**: GLM-4 Vision

## 🔧 API Usage

### Chat Completions
```bash
curl -N -X POST "http://localhost:8000/api/v1/chat/completions" \
-H "Content-Type: application/json" \
-d '{
  "messages": [{"role": "user", "content": "Write a quick sort in Python"}],
  "stream": true
}'
```

### Vision Completions
```bash
curl -X POST "http://localhost:8000/api/v1/vision/completions" \
-F "image=@path/to/your/image.jpg" \
-F "prompt=What's in this image?" \
-F "model=gpt-4-vision-preview"
```

## 🎬 Management Dashboard

After starting the service, visit `http://localhost:8000/admin` to access:

### Model Management
- Switch between active language and vision models
- Dynamically add new model configurations
- View model status and configuration info

### Model Testing
- **Language Model Testing**: Enter custom test messages on the left side of "Model Testing" tab
- **Visual Model Testing**: Upload images and mixed text-image testing on the right side
  - Upload images and enter descriptions for complete visual understanding tests
  - Images are automatically converted to base64 format, supporting common image formats

## 🚀 Deployment Options

### Development Environment

For development, we recommend using `uv` and `uvicorn` directly as it supports hot reload:

```bash
# Run with uv, no need to manually activate virtual environment
uv run uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Production Environment

In production, we don't recommend using `uvicorn` directly. Instead, use a more robust process manager.

#### Option 1: Gunicorn + Uvicorn (Recommended)

This is the golden combination for deploying Python ASGI applications (like FastAPI). Gunicorn acts as the process manager, responsible for starting and managing multiple Uvicorn worker processes, better utilizing server multi-core resources and ensuring service stability.

1. **Install gunicorn**:
    ```bash
    uv pip install gunicorn
    ```

2. **Start service with gunicorn**:
    ```bash
    # Start 4 Uvicorn worker processes
    gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app -b 0.0.0.0:8000
    ```
    - `-w 4`: Number of worker processes, usually recommended as `(2 * CPU cores) + 1`
    - `-k uvicorn.workers.UvicornWorker`: Tell Gunicorn to use Uvicorn worker class
    - `-b 0.0.0.0:8000`: Bind service address and port

#### Option 2: Docker Containerized Deployment

Packaging the entire application into a Docker image is the standard way to deploy in modern cloud environments. Here's a sample `Dockerfile`:

```dockerfile
# Use official Python base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install uv
RUN pip install uv

# Copy config files and dependency definition files
COPY pyproject.toml ./

# Install dependencies with uv
# --system means install to system Python environment, as it's isolated in container
RUN uv pip install --system -e .

# Copy all application code
COPY . .

# Expose port
EXPOSE 8000

# Container start command (using Gunicorn)
CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "main:app", "-b", "0.0.0.0:8000"]
```

## 📁 Project Structure

```
backend-llm/
├── app/
│   ├── admin/          # Gradio management interface
│   ├── api/            # API endpoints
│   ├── core/           # Core configuration
│   ├── schemas/        # Data models
│   └── services/       # Business logic
├── config/             # Model configurations
│   ├── models.yaml     # Model definitions
│   └── providers/      # Provider configs
├── docs/               # Provider-specific docs
├── main.py             # Application entry point
├── pyproject.toml      # Project dependencies
└── requirements.txt    # Python requirements
```

## 🔧 Configuration

### Environment Variables

Copy `.env.example` to `.env` and configure:

```bash
# Platform Configuration
PLATFORM_NAME=SK-LLM Gateway
DEBUG=false

# API Keys (Add your keys)
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key
GOOGLE_API_KEY=your_google_key
ALIBABA_API_KEY=your_alibaba_key
BAIDU_API_KEY=your_baidu_key
TENCENT_API_KEY=your_tencent_key
BYTEDANCE_API_KEY=your_bytedance_key
ZHIPU_API_KEY=your_zhipu_key
DEEPSEEK_API_KEY=your_deepseek_key
```

### Model Configuration

Edit `config/models.yaml` to customize available models:

```yaml
language_models:
  - provider: openai
    model: gpt-4
    display_name: GPT-4
    max_tokens: 8192
    
  - provider: anthropic
    model: claude-3-opus
    display_name: Claude 3 Opus
    max_tokens: 200000
```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 Links

- **Repository**: https://github.com/sihuangtech/sk-llm-gateway
- **Documentation**: [API_DOCS.md](API_DOCS.md)
- **Issue Tracker**: https://github.com/sihuangtech/sk-llm-gateway/issues

## 📞 Support

If you have any questions or need help, please:

1. Check the [documentation](API_DOCS.md)
2. Search existing [issues](https://github.com/sihuangtech/sk-llm-gateway/issues)
3. Create a new issue with detailed description

### Community
[![Discord](https://img.shields.io/badge/Discord-Join%20our%20Discord%20server-7289da?logo=discord&logoColor=white)](https://discord.gg/thWGWq7CwA)
[![QQ Group](https://img.shields.io/badge/QQ%20Group-Join%20our%20QQ%20group-12b7f5?logo=qq&logoColor=white)](https://qm.qq.com/q/WEBm0AkBKI)

---

**Star this repo if you find it helpful!**

## ⭐ Star History

[![Star History Chart](https://api.star-history.com/svg?repos=sihuangtech/sk-llm-gateway&type=date&legend=top-left)](https://www.star-history.com/#sihuangtech/sk-llm-gateway&type=date&legend=top-left)