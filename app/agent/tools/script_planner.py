from typing import Any
from app.agent.tools.base import BaseTool

class ScriptPlannerTool(BaseTool):
    name = "Script Planner"
    description = "根据用户输入的题材，生成AI短剧的基础企划，包括标题，卖点，世界观，角色和前5集大纲。"

    def run(self, arguments: dict[str, Any]) -> str:
        topic = arguments.get("topic", "")
        style = arguments.get("style", "爽剧")
        episode_count = arguments.get("episode_count", 5)

        return f"""
短剧企划生成结果：

题材：
{topic}

风格：
{style}

建议结构：
1. 标题： 围绕“逆袭， 神秘身份，强冲突”设计
2. 核心卖点： 前三秒必须有强钩子
3. 主角： 有明显弱点，但拥有隐藏能力
4. 反派： 压迫感强， 能持续制造冲突
5. 世界观： 简单，直观，方便AI生成画面
6. 节奏： 每集结尾必须留下悬念

前 {episode_count}集大纲：
第一集： 主角被羞辱/压迫，展示核心矛盾。
第二集：主角发现或展示隐藏能力。
第三集：反派升级压迫，主角第一次反击。
第四集： 出现更大的阴谋或新角色。
第五集： 主角阶段性胜利，但引出更强敌人。
"""