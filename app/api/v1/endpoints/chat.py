from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from app.core.model_manager import model_manager
from app.schemas.chat import ChatRequest
import asyncio

router = APIRouter()

async def stream_generator(stream):
    """将OpenAI的流式响应转换为FastAPI的生成器"""
    try:
        for chunk in stream:
            content = chunk.choices[0].delta.content
            if content:
                yield content
                await asyncio.sleep(0.01) # 防止事件过于密集
    except Exception as e:
        print(f"流式响应出错: {e}")
        yield "抱歉，处理流式响应时发生错误。"

@router.post("/chat/completions", summary="AI对话接口")
async def chat_completions(request: ChatRequest):
    """接收用户的对话请求，并以流式返回AI的回答。"""
    client = model_manager.get_active_client('language')
    if not client:
        raise HTTPException(status_code=503, detail="当前没有可用的语言模型服务，请在后台管理界面配置。")

    # 决定使用哪个模型名称
    # 优先使用客户端请求中指定的模型（适用于聚合平台）
    # 如果客户端未指定，则使用后台设置的默认激活模型
    model_to_use = request.model
    if not model_to_use:
        active_model_name = model_manager.active_models['active_language_model']
        model_config = model_manager.get_model_config(active_model_name)
        if not model_config:
            raise HTTPException(status_code=503, detail=f"激活的模型 '{active_model_name}' 配置不存在。")
        model_to_use = model_config['name']

    try:
        stream = client.chat.completions.create(
            model=model_to_use,
            messages=request.messages,
            stream=True
        )
        return StreamingResponse(stream_generator(stream), media_type="text/event-stream")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"请求大模型服务时出错: {str(e)}")
