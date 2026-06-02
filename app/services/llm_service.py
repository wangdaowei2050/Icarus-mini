from typing import Generator
from app.core.runtime.model_runtime import ModelRuntime

runtime = ModelRuntime()

def chat_with_llm(messages: list, model: str) -> Generator[str, None, None]:

    formatted_messages = [
        {
            "role": "system",
            "content": "你是Icarus Mini，一个有帮助的AI助手。"
        }
    ]

    for msg in messages:
        formatted_messages.append({
            "role": msg.role,
            "content": msg.content,
        })
    
    return runtime.invoke(
        model_name=model,
        messages=formatted_messages
    )