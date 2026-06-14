from app.agent.tools.registry import get_tool
from app.core.agent.state import AgentState

def execute(state: AgentState) -> AgentState:
    if state.intent != "use_tool":
        return state
    
    tool = get_tool(state.tool_name)

    if tool is None:
        state.tool_result = f"工具不存在：{state.tool_name}"
        return state
    
    state.tool_result = tool.run(state.tool_arguments)
    return state