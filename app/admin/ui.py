import gradio as gr
from app.core.model_manager import model_manager
from app.core.config import settings

def create_admin_ui():
    """创建并返回Gradio管理界面"""

    def get_providers():
        """获取所有厂商列表"""
        return model_manager.get_providers()
    
    def get_models_by_provider(provider: str, model_type: str):
        """根据厂商和模型类型获取模型列表"""
        provider_models = [m for m in model_manager.models if m['provider'] == provider and m['type'] == model_type]
        return [m['name'] for m in provider_models]
    
    def get_model_names(model_type: str):
        if model_type == 'language':
            return [m['name'] for m in model_manager.get_language_models()]
        else:
            return [m['name'] for m in model_manager.get_vision_models()]

    def update_language_model_dropdown(provider_name: str):
        """根据选择的厂商更新语言模型下拉列表"""
        if not provider_name:
            return gr.update(choices=[], value=None)
        models = get_models_by_provider(provider_name, 'language')
        current_lang = model_manager.active_models.get('active_language_model')
        # 如果当前激活的模型不在新列表中，则清空选择
        new_value = current_lang if current_lang in models else (models[0] if models else None)
        return gr.update(choices=models, value=new_value)
    
    def update_vision_model_dropdown(provider_name: str):
        """根据选择的厂商更新视觉模型下拉列表"""
        if not provider_name:
            return gr.update(choices=[], value=None)
        models = get_models_by_provider(provider_name, 'vision')
        current_vis = model_manager.active_models.get('active_vision_model')
        # 如果当前激活的模型不在新列表中，则清空选择
        new_value = current_vis if current_vis in models else (models[0] if models else None)
        return gr.update(choices=models, value=new_value)
    
    def update_active_models(lang_model, vis_model):
        model_manager.set_active_model('language', lang_model)
        model_manager.set_active_model('vision', vis_model)
        return f"激活模型已更新：\n语言模型: {lang_model}\n视觉模型: {vis_model}"

    def add_new_model(name, provider, api_key_env, base_url, model_type):
        if not all([name, provider, api_key_env, base_url, model_type]):
            return "所有字段均为必填项。", gr.update(), gr.update()
        
        new_model = {
            'name': name,
            'provider': provider,
            'api_key_env': api_key_env,
            'base_url': base_url,
            'type': model_type
        }
        result = model_manager.add_model(new_model)
        # 刷新模型列表
        model_manager.models = model_manager.load_models_from_yaml()
        
        return (
            result, 
            gr.update(choices=get_model_names('language')),
            gr.update(choices=get_model_names('vision'))
        )

    def test_language_model(test_message):
        """测试当前激活的语言模型"""
        try:
            client = model_manager.get_active_client('language')
            if not client:
                return "语言模型客户端初始化失败，请检查API密钥和环境变量配置。"
            
            active_model = model_manager.active_models.get('active_language_model')
            if not active_model:
                return "没有激活的语言模型，请先选择一个语言模型。"
            
            # 使用用户输入的测试消息，如果没有输入则使用默认消息
            message_content = test_message if test_message.strip() else "你好，这是一个测试消息，请回复\"测试成功\"即可。"
            
            # 发送测试请求
            response = client.chat.completions.create(
                model=active_model,
                messages=[{"role": "user", "content": message_content}],
                max_tokens=500,
                temperature=0.1
            )
            
            result = response.choices[0].message.content
            return f"✅ 语言模型测试成功！\n模型: {active_model}\n测试消息: {message_content}\n回复: {result}"
            
        except Exception as e:
            return f"❌ 语言模型测试失败！\n模型: {active_model if 'active_model' in locals() else '未知'}\n错误: {str(e)}"

    def test_vision_model(image_description, image_file=None):
        """测试当前激活的视觉模型"""
        try:
            client = model_manager.get_active_client('vision')
            if not client:
                return "视觉模型客户端初始化失败，请检查API密钥和环境变量配置。"
            
            active_model = model_manager.active_models.get('active_vision_model')
            if not active_model:
                return "没有激活的视觉模型，请先选择一个视觉模型。"
            
            # 构建消息内容
            if image_file is not None:
                # 如果有上传的图片，转换为base64
                import base64
                from PIL import Image
                import io
                
                # 将上传的图片转换为base64
                if isinstance(image_file, str) and image_file.startswith('data:image'):
                    # 已经是base64格式
                    image_base64 = image_file.split(',')[1]
                else:
                    # 处理上传的图片文件
                    image = Image.open(image_file)
                    # 转换格式并压缩
                    if image.mode != 'RGB':
                        image = image.convert('RGB')
                    
                    # 压缩图片大小
                    max_size = (1024, 1024)
                    image.thumbnail(max_size, Image.Resampling.LANCZOS)
                    
                    # 转换为base64
                    buffered = io.BytesIO()
                    image.save(buffered, format="JPEG", quality=85)
                    image_base64 = base64.b64encode(buffered.getvalue()).decode()
                
                messages = [{
                    "role": "user",
                    "content": [
                        {"type": "text", "text": image_description if image_description.strip() else "请描述这张图片的内容"},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"}}
                    ]
                }]
            else:
                # 如果没有图片，使用文本描述进行测试
                message_content = image_description if image_description.strip() else "描述一张图片的内容"
                messages = [{"role": "user", "content": message_content}]
            
            # 发送测试请求
            response = client.chat.completions.create(
                model=active_model,
                messages=messages,
                max_tokens=500,
                temperature=0.1
            )
            
            result = response.choices[0].message.content
            if image_file is not None:
                return f"✅ 视觉模型测试成功！\n模型: {active_model}\n问题: {image_description if image_description.strip() else '请描述这张图片的内容'}\n回复: {result}"
            else:
                return f"✅ 视觉模型测试成功！\n模型: {active_model}\n测试内容: {image_description if image_description.strip() else '描述一张图片的内容'}\n回复: {result}"
            
        except Exception as e:
            return f"❌ 视觉模型测试失败！\n模型: {active_model if 'active_model' in locals() else '未知'}\n错误: {str(e)}"

    with gr.Blocks(theme=gr.themes.Soft(), title=f"{settings.PLATFORM_NAME}") as admin_app:
        gr.Markdown(f"## {settings.PLATFORM_NAME}")

        with gr.Tabs():
            with gr.TabItem("模型选择与激活"):
                gr.Markdown("在此处选择当前线上服务使用的AI模型。")
                
                # 获取当前激活模型信息
                current_lang_model = model_manager.active_models.get('active_language_model')
                current_vis_model = model_manager.active_models.get('active_vision_model')
                current_lang_provider = model_manager.active_models.get('active_language_model_provider')
                current_vis_provider = model_manager.active_models.get('active_vision_model_provider')
                
                # 语言模型选择区域
                gr.Markdown("### 语言模型选择")
                with gr.Row():
                    lang_provider_dd = gr.Dropdown(
                        label="选择语言模型厂商", 
                        choices=get_providers(),
                        value=current_lang_provider,
                        interactive=True
                    )
                    active_lang_model_dd = gr.Dropdown(
                        label="选择语言模型", 
                        choices=get_models_by_provider(current_lang_provider, 'language') if current_lang_provider else [], 
                        value=current_lang_model,
                        interactive=True
                    )
                
                # 视觉模型选择区域
                gr.Markdown("### 视觉模型选择")
                with gr.Row():
                    vis_provider_dd = gr.Dropdown(
                        label="选择视觉模型厂商", 
                        choices=get_providers(),
                        value=current_vis_provider,
                        interactive=True
                    )
                    active_vis_model_dd = gr.Dropdown(
                        label="选择视觉模型", 
                        choices=get_models_by_provider(current_vis_provider, 'vision') if current_vis_provider else [],
                        value=current_vis_model,
                        interactive=True
                    )
                
                save_button = gr.Button("保存并激活设置", variant="primary")
                status_output = gr.Textbox(label="操作结果", interactive=False, lines=5, max_lines=10)

            with gr.TabItem("动态添加新模型"):
                gr.Markdown("在此处添加新的OpenAI兼容模型到系统配置中。")
                with gr.Row():
                    new_model_name = gr.Textbox(label="模型名称 (唯一)")
                    new_model_provider = gr.Textbox(label="供应商 (如 ZhipuAI)")
                with gr.Row():
                    new_model_key_env = gr.Textbox(label="API Key 环境变量名")
                    new_model_base_url = gr.Textbox(label="Base URL")
                new_model_type = gr.Dropdown(label="模型类型", choices=['language', 'vision'])
                
                add_button = gr.Button("添加新模型", variant="primary")
                add_status_output = gr.Textbox(label="操作结果", interactive=False, lines=5, max_lines=10)

            with gr.TabItem("模型测试"):
                gr.Markdown("测试当前激活的语言模型和视觉模型是否可用。")
                
                # 显示当前激活的模型信息
                current_lang_model = model_manager.active_models.get('active_language_model')
                current_vis_model = model_manager.active_models.get('active_vision_model')
                
                gr.Markdown(f"**当前激活模型：**")
                gr.Markdown(f"- 语言模型: {current_lang_model or '未设置'}")
                gr.Markdown(f"- 视觉模型: {current_vis_model or '未设置'}")
                
                # 左右结构布局：语言模型在左，视觉模型在右
                with gr.Row():
                    # 左侧：语言模型测试区域
                    with gr.Column(scale=1):
                        gr.Markdown("### 🗣️ 语言模型测试")
                        with gr.Row():
                            test_message_input = gr.Textbox(
                                label="测试消息（可选）",
                                placeholder="输入测试消息，留空使用默认消息",
                                lines=2,
                                scale=4
                            )
                            test_lang_button = gr.Button("测试", variant="primary", scale=1)
                        test_lang_output = gr.Textbox(label="测试结果", lines=10)
                    
                    # 右侧：视觉模型测试区域
                    with gr.Column(scale=1):
                        gr.Markdown("### 👁️ 视觉模型测试")
                        image_description_input = gr.Textbox(
                            label="图片描述（可选）",
                            placeholder="输入图片描述，留空使用默认描述",
                            lines=2
                        )
                        with gr.Row():
                            image_file_input = gr.File(
                                label="上传图片（可选）",
                                file_types=["image"],
                                scale=3
                            )
                            test_vis_button = gr.Button("测试", variant="primary", scale=1)
                        test_vis_output = gr.Textbox(label="测试结果", lines=10)

        # 绑定事件 - 厂商选择触发模型列表更新
        lang_provider_dd.change(
            fn=update_language_model_dropdown,
            inputs=[lang_provider_dd],
            outputs=[active_lang_model_dd]
        )
        vis_provider_dd.change(
            fn=update_vision_model_dropdown,
            inputs=[vis_provider_dd],
            outputs=[active_vis_model_dd]
        )
        
        # 绑定事件 - 保存设置
        save_button.click(
            fn=update_active_models, 
            inputs=[active_lang_model_dd, active_vis_model_dd], 
            outputs=status_output
        )
        add_button.click(
            fn=add_new_model,
            inputs=[new_model_name, new_model_provider, new_model_key_env, new_model_base_url, new_model_type],
            outputs=[add_status_output, active_lang_model_dd, active_vis_model_dd]
        )
        
        # 绑定事件 - 模型测试
        test_lang_button.click(
            fn=test_language_model,
            inputs=[test_message_input],
            outputs=test_lang_output
        )
        test_vis_button.click(
            fn=test_vision_model,
            inputs=[image_description_input, image_file_input],
            outputs=test_vis_output
        )

    return admin_app
