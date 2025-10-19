import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    # 从.env文件中读取环境变量 - OpenAI兼容格式
    ZHIPU_API_KEY: str | None = os.getenv("ZHIPU_API_KEY")
    MOONSHOT_API_KEY: str | None = os.getenv("MOONSHOT_API_KEY")
    DEEPSEEK_API_KEY: str | None = os.getenv("DEEPSEEK_API_KEY")
    DASHSCOPE_API_KEY: str | None = os.getenv("DASHSCOPE_API_KEY")
    QIANFAN_API_KEY: str | None = os.getenv("QIANFAN_API_KEY")  # 简化：单个API Key
    HUNYUAN_API_KEY: str | None = os.getenv("HUNYUAN_API_KEY")  # 简化：单个API Key
    VOLCANO_API_KEY: str | None = os.getenv("VOLCANO_API_KEY")  # 简化：单个API Key
    SILICONFLOW_API_KEY: str | None = os.getenv("SILICONFLOW_API_KEY")
    OLLAMA_API_KEY: str | None = os.getenv("OLLAMA_API_KEY")

    # 平台配置
    PLATFORM_NAME: str = os.getenv("PLATFORM_NAME", "彩旗工作室大模型调用管理平台")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# 创建一个全局的配置实例
settings = Settings()
