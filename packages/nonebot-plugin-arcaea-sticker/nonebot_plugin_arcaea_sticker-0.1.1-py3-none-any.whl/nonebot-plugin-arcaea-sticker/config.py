from pydantic import BaseModel, Extra
from nonebot import get_driver

class Config(BaseModel, extra=Extra.ignore):
    arcaea_reply: bool = True
    arcaea_use_cache: bool = True

plugin_config = Config.parse_obj(get_driver().config)