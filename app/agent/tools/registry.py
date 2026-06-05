from app.agent.tools.script_planner import ScriptPlannerTool
from app.agent.tools.character_builder import CharacterBuilderTool

TOOLS = {
    "script_planner": ScriptPlannerTool(),
    "character_builder": CharacterBuilderTool(),
}

def get_tool(name: str):
    return TOOLS.get(name)

def list_tools():
    return [
        {
            "name": tool.name,
            "description": tool.description
        } for tool in TOOLS.values()
    ]

