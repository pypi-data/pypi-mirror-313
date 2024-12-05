from mmisp.db.models.correlation import OverCorrelatingValue
from mmisp.util.uuid import uuid


def generate_over_correlating_value() -> OverCorrelatingValue:
    return OverCorrelatingValue(
        value=uuid(),
        occurrence=1,
    )
