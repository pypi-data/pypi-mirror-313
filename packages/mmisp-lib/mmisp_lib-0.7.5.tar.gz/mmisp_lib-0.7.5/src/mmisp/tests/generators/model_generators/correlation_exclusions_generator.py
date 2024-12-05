from mmisp.db.models.correlation import CorrelationExclusions
from mmisp.util.uuid import uuid


def generate_correlation_exclusions() -> CorrelationExclusions:
    return CorrelationExclusions(value=uuid(), comment="test", from_json=0)
