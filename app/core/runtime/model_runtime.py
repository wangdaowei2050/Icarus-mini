from typing import Generator
from app.core.runtime.models import MODEL_SCHEMA
from app.core.runtime.provider_registry import PROVIDER_REGISTRY


# 收到 model_name
# ↓
# 去 MODEL_SCHEMAS 找模型说明书
# ↓
# 通过 schema.provider 找 provider client
# ↓
# 调用 provider client.invoke_llm()
# ↓
# 返回模型回复

class ModelRuntime:
    def invoke(self, model_name: str, messages: list) -> Generator[str, None, None]:
        schema = MODEL_SCHEMA[model_name]

        provider_client_class = PROVIDER_REGISTRY[schema.provider]
        api_key = schema.api_key
        base_url = schema.base_url
        provider_client = provider_client_class(api_key=api_key, base_url=base_url)

        return provider_client.invoke_llm(
            model_name=schema.model_name,
            messages=messages,
        )

