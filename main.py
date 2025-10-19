from fastapi import FastAPI
import gradio as gr
from app.api.v1.api import api_router
from app.admin.ui import create_admin_ui

# 创建FastAPI应用
app = FastAPI(
    title="彩旗工作室大模型调用管理平台",
    description="一个支持多厂商、多模型的大语言模型统一管理平台，提供统一的API接口和模型管理功能。",
    version="1.0.0"
)

# 包含v1版本的API路由
app.include_router(api_router, prefix="/api/v1")

# 创建Gradio管理界面
gradio_app = create_admin_ui()

# 将Gradio应用挂载到FastAPI上
# 这样可以通过访问 /admin 来进入管理后台
app = gr.mount_gradio_app(app, gradio_app, path="/admin")

@app.get("/", summary="服务健康检查", tags=["Default"])
def read_root():
    """检查服务是否正常运行，并告知后台管理路径。"""
    return {
        "status": "LLM统一管理平台 is running.",
        "admin_panel": "Access the admin panel at /admin",
        "description": "一个支持多厂商、多模型的大语言模型统一管理平台"
    }