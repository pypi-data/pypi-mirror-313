from datetime import datetime

from pydantic import BaseModel

from mmisp.lib.distribution import DistributionLevels


class GetAllSearchGalaxiesAttributes(BaseModel):
    id: int
    uuid: str
    name: str
    type: str
    description: str
    version: str
    icon: str
    namespace: str
    kill_chain_order: str | None = None
    enabled: bool
    local_only: bool
    created: datetime | str
    modified: datetime | str
    org_id: int
    orgc_id: int
    default: bool
    distribution: DistributionLevels
