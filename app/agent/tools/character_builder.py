from typing import Any
from app.agent.tools.base import BaseTool

class CharacterBuilderTool(BaseTool):
    name = "Character Builder"
    description = "根据短剧题材生成主角，反派，配角，人物关系和视觉风格。"

    def run(self, arguments: dict[str, Any]) -> str:
        topic = arguments.get("topic", "")
        character_count = arguments.get("character_count", 5)

        return f"""
角色设定生成结果：
题材：
{topic}

角色数量：
{character_count}

主角：
- 身份：被低估的普通人/学徒/底层角色
- 核心欲望：证明自己，夺回尊严
- 隐藏能力：拥有某种被忽视但极强的技术或知识
- 弱点：不善表达、资源不足、被权力结构压制

反派：
- 身份：贵族、资本方、上级、竞争者
- 压迫方式：羞辱、夺取成果、封锁机会
- 爽点作用：制造强压迫，让主角反击更有快感

重要配角：
- 盟友：最初不相信主角，后来被主角能力折服
- 见证者：负责让观众看到主角的成长
- 关键人物：掌握秘密或资源，推动剧情升级

人物关系：
主角被反派压制，但通过专业能力逐步逆袭。
每一集都要让人物关系发生一次变化。

视觉风格：
根据题材强化服装、场景、道具和身份符号。
"""