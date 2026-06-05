import json
from app.agent.tools.registry import get_tool
from app.services.llm_service import chat_with_llm
from app.schemas.chat import ChatMessage

DEBUG_AGENT = True

SYSTEM_PROMPT = """
你是 Icarus Mini 的AI短剧平台Agent。
你可以直接回答，也可以调用工具。
当前可用工具：
1. script_planner
用途： 根据用户输入的题材，生成AI短剧企划。
如果你认为需要调用工具，请严格只输出JSON，不要输出其他文字：
{
    "tool": "script_planner",
    "arguments": {
        "topic": "用户想做的短剧题材",
        "style": "爽剧/悬疑/校园/中世纪/赛博朋克/古风",
        "episode_count": 5
        }
}
2. character_builder
用途：根据短剧题材生成主角、反派、配角、人物关系和视觉风格。
如果需要调用 character_builder，请输出：

{
  "tool": "character_builder",
  "arguments": {
    "topic": "用户想做的短剧题材",
    "character_count": 3
  }
}
如果不需要调用工具，就正常回答。
"""

def run_agent(messages: list[ChatMessage], model: str):
    agent_messages = [
        ChatMessage(role="system", content=SYSTEM_PROMPT),
        *messages,
    ]

    first_reply = ""

    for chunk in chat_with_llm(model=model, messages=agent_messages):
        first_reply += chunk
    
    try:
        tool_call = json.loads(first_reply)
    except Exception:
        yield first_reply
        return
    
    tool_name = tool_call.get("tool")
    arguments = tool_call.get("arguments", {})

    tool = get_tool(tool_name)

    if tool is None:
        yield first_reply
        return
    
    tool_result = tool.run(arguments)

    if DEBUG_AGENT:
        yield f"\n\n[Tool call]\n工具： {tool_name}\n参数： {arguments}\n\n"
        yield f"[Tool result]\n{tool_result}\n\n"

    final_messages = [
        *agent_messages,
        ChatMessage(role="assistant", content=first_reply),
        ChatMessage(role="tool", content=f"工具执行结果如下：{tool_result}请把它整理成适合用户阅读的短剧企划方案。"),
    ]

    for chunk in chat_with_llm(final_messages, model=model):
        yield chunk