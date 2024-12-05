import time

from mmisp.db.models.sighting import Sighting
from mmisp.lib.uuid import uuid
from mmisp.tests.generators.object_generator import generate_random_str


def generate_sighting(event_id: int, attribute_id: int, org_id: int) -> Sighting:
    return Sighting(
        uuid=uuid(),
        attribute_id=attribute_id,
        event_id=event_id,
        org_id=org_id,
        date_sighting=int(time.time()),
        source=generate_random_str(),
        type=0,
    )
