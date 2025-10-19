import yaml
import json
import os
import glob
from typing import List, Dict, Any, Optional
from openai import OpenAI
from app.core.config import settings

# 定义配置文件的路径
MODELS_CONFIG_PATH = "config/models.yaml"
PROVIDERS_CONFIG_PATH = "config/providers/*.yaml"
ACTIVE_MODELS_PATH = "config/active_models.json"

class ModelManager:
    """管理和切换AI模型"""

    def __init__(self):
        self.providers = self.load_providers()
        self.models = self.load_all_models()
        self.active_models = self.load_active_models()

    def load_providers(self) -> Dict[str, Dict[str, Any]]:
        """从providers目录加载所有厂商配置"""
        providers = {}
        provider_files = glob.glob(PROVIDERS_CONFIG_PATH)
        
        for file_path in provider_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    provider_config = yaml.safe_load(f)
                    provider_name = provider_config.get('provider')
                    if provider_name:
                        providers[provider_name] = provider_config
            except Exception as e:
                print(f"加载厂商配置文件 {file_path} 失败: {e}")
        
        return providers

    def load_all_models(self) -> List[Dict[str, Any]]:
        """从厂商配置中加载所有模型"""
        all_models = []
        
        # 从models.yaml获取厂商基本信息
        try:
            with open(MODELS_CONFIG_PATH, 'r', encoding='utf-8') as f:
                main_config = yaml.safe_load(f)
                # 直接用厂商名称作为key，简单直观
                providers_info = {p['name']: p for p in main_config.get('providers', [])}
        except Exception as e:
            print(f"加载主配置文件失败: {e}")
            return []
        
        # 合并厂商信息和模型配置
        for provider_name, provider_config in self.providers.items():
            # 直接用厂商名称匹配，无需转换
            provider_info = providers_info.get(provider_name, {})
            
            # 添加语言模型
            for model in provider_config.get('models', {}).get('language', []):
                all_models.append({
                    'name': model['name'],
                    'display_name': model.get('display_name', model['name']),
                    'provider': provider_name,
                    'type': 'language',
                    'description': model.get('description', ''),
                    'api_key_env': provider_info.get('api_key_env'),
                    'base_url': provider_info.get('base_url')
                })
            
            # 添加视觉模型
            for model in provider_config.get('models', {}).get('vision', []):
                all_models.append({
                    'name': model['name'],
                    'display_name': model.get('display_name', model['name']),
                    'provider': provider_name,
                    'type': 'vision',
                    'description': model.get('description', ''),
                    'api_key_env': provider_info.get('api_key_env'),
                    'base_url': provider_info.get('base_url')
                })
        
        return all_models

    def load_models_from_yaml(self) -> List[Dict[str, Any]]:
        """从YAML文件中加载模型配置（兼容旧格式）"""
        try:
            with open(MODELS_CONFIG_PATH, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
                # 如果新格式包含providers，则从providers目录加载
                if 'providers' in data:
                    return self.load_all_models()
                # 否则使用旧格式
                return data.get('models', [])
        except FileNotFoundError:
            return []

    def add_model(self, new_model: Dict[str, Any]) -> str:
        """添加一个新模型并保存"""
        if any(m['name'] == new_model['name'] for m in self.models):
            return f"模型名称 '{new_model['name']}' 已存在，请使用其他名称。"
        self.models.append(new_model)
        # 注意：新的配置文件结构不支持直接保存单个模型
        return f"模型 '{new_model['name']}' 添加成功。（注意：新的配置文件结构不支持自动保存）"

    def load_active_models(self) -> Dict[str, str]:
        """加载当前激活的模型"""
        try:
            with open(ACTIVE_MODELS_PATH, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            # 如果文件不存在或为空，则返回默认值
            lang_models = self.get_language_models()
            vis_models = self.get_vision_models()
            
            default_lang_model = lang_models[0] if lang_models else None
            default_vis_model = vis_models[0] if vis_models else None
            
            result = {
                "active_language_model": default_lang_model['name'] if default_lang_model else None,
                "active_vision_model": default_vis_model['name'] if default_vis_model else None
            }
            
            # 如果有默认模型，也设置厂商信息
            if default_lang_model:
                result["active_language_model_provider"] = default_lang_model['provider']
            if default_vis_model:
                result["active_vision_model_provider"] = default_vis_model['provider']
                
            return result

    def save_active_models(self):
        """保存当前激活的模型"""
        with open(ACTIVE_MODELS_PATH, 'w', encoding='utf-8') as f:
            json.dump(self.active_models, f, indent=4)

    def get_language_models(self) -> List[Dict[str, Any]]:
        """获取所有语言模型"""
        return [m for m in self.models if m['type'] == 'language']

    def get_vision_models(self) -> List[Dict[str, Any]]:
        """获取所有视觉模型"""
        return [m for m in self.models if m['type'] == 'vision']

    def set_active_model(self, model_type: str, model_name: str):
        """设置激活的模型"""
        # 获取模型配置以确定厂商
        model_config = self.get_model_config(model_name)
        if model_config:
            provider = model_config.get('provider')
            if model_type == 'language':
                self.active_models['active_language_model'] = model_name
                self.active_models['active_language_model_provider'] = provider
            elif model_type == 'vision':
                self.active_models['active_vision_model'] = model_name
                self.active_models['active_vision_model_provider'] = provider
            self.save_active_models()

    def get_model_config(self, model_name: str) -> Optional[Dict[str, Any]]:
        """根据名称获取模型配置"""
        return next((m for m in self.models if m['name'] == model_name), None)

    def get_active_client(self, model_type: str) -> Optional[OpenAI]:
        """获取当前激活模型的OpenAI客户端"""
        active_model_name = self.active_models.get(f'active_{model_type}_model')
        if not active_model_name:
            return None
        
        config = self.get_model_config(active_model_name)
        if not config:
            return None

        api_key = getattr(settings, config['api_key_env'], None)
        if not api_key:
            print(f"警告: 环境变量 {config['api_key_env']} 未设置.")
            return None

        return OpenAI(api_key=api_key, base_url=config['base_url'])

    def get_provider_models(self, provider_name: str) -> List[Dict[str, Any]]:
        """获取指定厂商的所有模型"""
        return [m for m in self.models if m['provider'] == provider_name]

    def get_providers(self) -> List[str]:
        """获取所有厂商名称"""
        return list(set(m['provider'] for m in self.models))

# 创建一个全局的ModelManager实例
model_manager = ModelManager()
