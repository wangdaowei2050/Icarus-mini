from app.core.runtime.model_schema import ModelSchema
from app.core.config import QWEN_API_KEY, QWEN_BASE_URL, DEEPSEEK_API_KEY, DEEPSEEK_BASE_URL

MODEL_SCHEMA = {
    "qwen3.7-max": ModelSchema(
        provider='dashscope',
        model_name='qwen3.7-max',
        api_key=QWEN_API_KEY,
        base_url=QWEN_BASE_URL,
        support_stream=True,
        support_tool_call=True,
        context_size=32768,
    ),
    "deepseek-v4-flash": ModelSchema(
        provider='deepseek',
        model_name='deepseek-v4-flash',
        api_key=DEEPSEEK_API_KEY,
        base_url=DEEPSEEK_BASE_URL,
        support_stream=True,
        support_tool_call=True,
        context_size=32768,
    ),
}