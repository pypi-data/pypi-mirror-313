from mmisp.db.models.correlation import DefaultCorrelation


# ids don't match to the actual ids in the database, its complex, and I am lazy
def generate_default_correlation() -> DefaultCorrelation:
    return DefaultCorrelation(
        attribute_id=1,
        object_id=1,
        event_id=1,
        org_id=1,
        distribution=1,
        object_distribution=1,
        event_distribution=1,
        sharing_group_id=1,
        object_sharing_group_id=1,
        event_sharing_group_id=1,
        attribute_id_1=1,
        object_id_1=1,
        event_id_1=1,
        org_id_1=1,
        distribution_1=1,
        object_distribution_1=1,
        event_distribution_1=1,
        sharing_group_id_1=1,
        object_sharing_group_id_1=1,
        event_sharing_group_id_1=1,
    )
