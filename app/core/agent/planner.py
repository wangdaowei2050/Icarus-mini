import json
from app.schemas.chat import ChatMessage
from app.services.llm_service import chat_with_llm
from app.core.agent.state import AgentState
from app.core.runs.redis_run_store import RedisRunStore

SYSTEM_PROMPT = """
你是 Icarus Mini 的 AI短剧平台 Planner。

你的任务不是直接回答用户，而是判断用户想做什么。

当前支持的动作：

1. direct_answer
适合：普通聊天、解释概念、无需调用工具的问题。

2. use_tool
适合：用户想生成短剧企划、角色设定、分集大纲等。

如果需要调用工具，请严格输出 JSON：

{
  "intent": "use_tool",
  "tool": "script_planner",
  "arguments": {
    "topic": "用户的短剧题材",
    "style": "爽剧",
    "episode_count": 5
  }
}

如果不需要工具，请输出：

{
  "intent": "direct_answer"
}
"""

def plan(state: AgentState) -> AgentState:
    memory_text = "\n".join(state.short_memory)
    planner_messages = [
        ChatMessage(role="system", content=SYSTEM_PROMPT + f"\n\n用户短期记忆:\n{memory_text}"),
        *state.messages,
    ]

    reply = ""
    for chunk in chat_with_llm(model=state.model, messages=planner_messages):
        reply += chunk

    try:
        data = json.loads(reply)
    except Exception:
        state.intent = "direct_answer"
        return state
    
    state.intent = data.get("intent", "direct_answer")
    state.tool_name = data.get("tool")
    state.tool_arguments = data.get("arguments", {})

    run_store = RedisRunStore()

    return state
