from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from app.core.model_manager import model_manager
import base64

router = APIRouter()

@router.post("/vision/completions", summary="视觉模型对话接口")
async def vision_completions(model: str | None = Form(None), image: UploadFile = File(...)):
    """接收上传的图片和文本描述，调用视觉模型进行分析，返回识别结果。支持客户端动态指定模型。"""
    client = model_manager.get_active_client('vision')
    if not client:
        raise HTTPException(status_code=503, detail="当前没有可用的视觉模型服务，请在后台管理界面配置。")

    # 决定使用哪个模型名称
    model_to_use = model
    if not model_to_use:
        active_model_name = model_manager.active_models['active_vision_model']
        model_config = model_manager.get_model_config(active_model_name)
        if not model_config:
            raise HTTPException(status_code=503, detail=f"激活的视觉模型 '{active_model_name}' 配置不存在。")
        model_to_use = model_config['name']

    # 读取图片内容并进行Base64编码
    contents = await image.read()
    base64_image = base64.b64encode(contents).decode('utf-8')
    image_url = f"data:{image.content_type};base64,{base64_image}"

    try:
        response = client.chat.completions.create(
            model=model_to_use,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "这张图片里最主要的物体是什么？请用中文回答，并用一句话描述它。"},
                        {
                            "type": "image_url",
                            "image_url": {"url": image_url},
                        },
                    ],
                }
            ],
            max_tokens=300,
        )
        
        ai_content = response.choices[0].message.content

        # 此处仅为简化，实际应解析AI返回内容并构造成Flutter App需要的格式
        return {
            "recognition_id": response.id,
            "objects": [
                {
                    "name": ai_content.split('\n')[0],
                    "description": ai_content
                }
            ]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"请求视觉大模型服务时出错: {str(e)}")
