from enum import Enum

from pydantic import BaseModel, confrozenset, conlist

from mmisp.plugins.plugin_info import PluginInfo


class EnrichmentPluginType(str, Enum):
    """
    Enum describing all possible enrichment plugin types.
    """

    EXPANSION = "expansion"
    """Enrichment Plugins of this type generate new attributes that can be attached to a MISP-Event
    to add additional information permanently."""
    HOVER = "hover"
    """Enrichment Plugins of this type generate information that is usually only displayed once
    and should not be stored permanently in the database."""


class PluginIO(BaseModel):
    """
    Encapsulates information about the accepted and returned attribute types of a plugin.
    """

    class Config:
        allow_mutation = False
        anystr_strip_whitespace = True
        min_anystr_length = 1

    INPUT: conlist(str, min_items=1)
    """Attribute types accepted by the Enrichment Plugin."""
    OUTPUT: conlist(str, min_items=1)
    """Attribute types returned by the Enrichment Plugin."""


class EnrichmentPluginInfo(PluginInfo):
    ENRICHMENT_TYPE: confrozenset(EnrichmentPluginType, min_items=1)
    """The type of the enrichment plugin."""
    MISP_ATTRIBUTES: PluginIO
    """The accepted and returned types of attributes of the enrichment plugin."""
