from nonebot.plugin import PluginMetadata

from .config import Config
from .matcher import *

__plugin_meta__ = PluginMetadata(
    name="Arcaea表情包生成器",
    description="生成Arcaea风格的表情包",
    usage="""
    基础指令：
    - arc <角色> <文字> - 生成表情包
    - arc -h - 显示帮助
    - arc - 进入交互模式
    """,
    type="application",
    homepage="https://github.com/JQ-28/nonebot-plugin-arcaea",
    config=Config,
    supported_adapters={"~onebot.v11"},
)