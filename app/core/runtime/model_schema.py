from pydantic import BaseModel

class ModelSchema(BaseModel):
    provider: str
    model_name: str
    api_key: str
    base_url: str
    support_stream: bool = False
    support_tool_call: bool = False
    context_size: int = 8192