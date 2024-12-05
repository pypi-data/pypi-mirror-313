from mmisp.db.models.correlation import CorrelationValue
from mmisp.util.uuid import uuid


def generate_correlation_value() -> CorrelationValue:
    return CorrelationValue(
        value=uuid(),
    )
