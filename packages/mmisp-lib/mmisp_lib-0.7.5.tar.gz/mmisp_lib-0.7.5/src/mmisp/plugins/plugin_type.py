from enum import Enum


class PluginType(str, Enum):
    """
    Enum encapsulating possible plugin types.
    """

    CORRELATION = "correlation"
    """Type for plugins specifically made for correlation jobs."""
    ENRICHMENT = "enrichment"
    """Type for plugins specifically made for enrichment jobs."""
