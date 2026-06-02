from app.core.runtime.clients.openai_compatible import OpenAICompatibleClient

PROVIDER_REGISTRY = {
    "dashscope": OpenAICompatibleClient,
    "deepseek": OpenAICompatibleClient,
}