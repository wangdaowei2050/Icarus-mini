from app.schemas.chat import ChatMessage
from app.services.llm_service import chat_with_llm
from app.core.agent.state import AgentState
from app.core.agent.planner import plan
from app.core.agent.executor import execute
from app.core.memory.manager import MemoryManager

import uuid
from app.core.runs.redis_run_store import RedisRunStore


def run_agent(messages: list[ChatMessage], model: str, conversation_id: int):

    run_id = str(uuid.uuid4())
    run_store = RedisRunStore()

    run_store.create_run(run_id=run_id, conversation_id=conversation_id, user_id=1)

    run_store.add_event(run_id, "run_started", {"conversation_id": conversation_id})

    memory_manager = MemoryManager()
    state = AgentState(
        conversation_id=conversation_id,
        model=model,
        messages=messages,
    )
    state.short_memory = memory_manager.read_short(state.user_id)

    state = plan(state)
    if state.intent == "use_tool":
        state = execute(state)

        final_messages = [
            *messages,
            ChatMessage(role="tool", content=f"""
                        工具执行结果如下：
                        {state.tool_result}
                        请根据工具结果，整理成适合用户阅读的AI短剧输出。""")
        ]

        for chunk in chat_with_llm(model=model, messages=final_messages):
            state.final_answer += chunk
            yield chunk

        return
    
    for chunk in chat_with_llm(model=model, messages=messages):
        state.final_answer +=chunk
        yield chunk

    memory_manager.write_short(state.user_id, f"用户输入：{messages[-1].content}")
    memory_manager.write_short(state.user_id, f"助手回答：{state.final_answer[:200]}")


    