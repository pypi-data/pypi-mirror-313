from langchain_openai import ChatOpenAI
from .config_manager import get_active_model

def get_model():
    active_config = get_active_model()
    return ChatOpenAI(
        model=active_config.get('model', ""),
        base_url=active_config.get('base_url', ''),
        temperature=active_config.get('temperature', 0.2),
        api_key=active_config.get('api_key', ''),
    )
