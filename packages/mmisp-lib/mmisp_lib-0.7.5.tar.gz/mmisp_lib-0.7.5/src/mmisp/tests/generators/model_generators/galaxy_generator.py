from datetime import datetime

from mmisp.db.models.galaxy import Galaxy
from mmisp.lib.distribution import DistributionLevels


def generate_galaxy() -> Galaxy:
    return Galaxy(
        name="test galaxy",
        type="test type",
        description="test",
        version="version",
        kill_chain_order="test kill_chain_order",
        org_id=0,
        orgc_id=0,
        distribution=DistributionLevels.ALL_COMMUNITIES,
        created=datetime.now(),
        modified=datetime.now(),
    )
