from pathlib import Path
from pydantic import BaseModel, Extra
from nonebot import get_driver

# 插件目录
PLUGIN_DIR = Path(__file__).parent

# 资源目录
RESOURCE_DIR = PLUGIN_DIR / "resources"
FONT_DIR = RESOURCE_DIR / "fonts"

# 角色颜色配置
CHARACTER_COLORS = {
    "hikari": {"fill": "#33A6B8", "stroke": "#FFFFFF"},
    "tairitsu": {"fill": "#FF4B4B", "stroke": "#FFFFFF"},
    "kou": {"fill": "#FF98CA", "stroke": "#FFFFFF"},
    "sapphire": {"fill": "#4455DD", "stroke": "#FFFFFF"},
    "lethe": {"fill": "#8800FF", "stroke": "#FFFFFF"},
    "toa": {"fill": "#FF6699", "stroke": "#FFFFFF"},
    "luna": {"fill": "#CC88FF", "stroke": "#FFFFFF"},
    "ayu": {"fill": "#FF9933", "stroke": "#FFFFFF"},
    "grievous": {"fill": "#FF3366", "stroke": "#FFFFFF"},
    "sia": {"fill": "#66CCFF", "stroke": "#FFFFFF"},
    "isabelle": {"fill": "#FF99CC", "stroke": "#FFFFFF"},
    "ilith": {"fill": "#CC3366", "stroke": "#FFFFFF"},
    "eto": {"fill": "#FF9999", "stroke": "#FFFFFF"},
    "alice": {"fill": "#99CCFF", "stroke": "#FFFFFF"},
    "amane": {"fill": "#FFCC66", "stroke": "#FFFFFF"},
    "maya": {"fill": "#CC99FF", "stroke": "#FFFFFF"},
    "mir": {"fill": "#FF6666", "stroke": "#FFFFFF"},
    "vita": {"fill": "#66FF99", "stroke": "#FFFFFF"},
    "shirabe": {"fill": "#FF99FF", "stroke": "#FFFFFF"},
    "saya": {"fill": "#99FF99", "stroke": "#FFFFFF"},
    "kanae": {"fill": "#9999FF", "stroke": "#FFFFFF"},
}

# 默认颜色
DEFAULT_COLORS = {
    "fill": "#FFFFFF",  # 白色填充
    "stroke": "#000000"  # 黑色描边
}

class Config(BaseModel):
    """Plugin Config
    
    Attributes:
        arcaea_reply (bool): 是否回复消息
        arcaea_use_cache (bool): 是否使用缓存
    """
    arcaea_reply: bool = True
    arcaea_use_cache: bool = True

    class Config:
        extra = Extra.ignore

# 获取全局配置
try:
    plugin_config = Config.parse_obj(get_driver().config.dict())
except Exception as e:
    plugin_config = Config()  # 使用默认配置