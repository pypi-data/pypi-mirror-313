from typing import Optional

from pydantic import BaseModel, constr

from mmisp.plugins.plugin_type import PluginType


class PluginInfo(BaseModel):
    """
    Encapsulates information about a plugin.
    """

    class Config:
        anystr_strip_whitespace = True
        allow_mutation = False

    NAME: constr(min_length=1)
    """Name of the plugin"""
    PLUGIN_TYPE: PluginType
    """Type of the plugin"""
    DESCRIPTION: Optional[str] = None
    """Description of the plugin"""
    AUTHOR: Optional[str] = None
    """Author who wrote the plugin"""
    VERSION: Optional[str] = None
    """Version of the plugin"""
