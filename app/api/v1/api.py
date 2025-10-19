from fastapi import APIRouter
from app.api.v1.endpoints import chat, vision

api_router = APIRouter()

# 包含来自不同模块的路由
api_router.include_router(chat.router, prefix="", tags=["Chat"])
api_router.include_router(vision.router, prefix="", tags=["Vision"])
