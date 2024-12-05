from sqlalchemy.ext.asyncio import AsyncSession

from mmisp.api_schemas.galaxy_clusters import AddUpdateGalaxyElement
from mmisp.db.models.galaxy_cluster import GalaxyCluster, GalaxyElement


async def update_galaxy_cluster_elements(
    db: AsyncSession, galaxy_cluster: GalaxyCluster, new: list[AddUpdateGalaxyElement]
) -> None:
    """Update the relationship of GalaxyCluster to GalaxyElements as defined by new_dict"""
    old = [ge.asdict(omit={"galaxy_cluster_id"}) for ge in galaxy_cluster.galaxy_elements]

    maybe_updated_dict = {item.id: item.dict() for item in new if item.id is not None}
    added_dict = [item for item in new if item.id is None]
    new_ids = {item.id for item in new if item.id is not None}
    old_ids = {item["id"] for item in old if "id" in item}

    to_delete = old_ids - new_ids
    if new_ids - old_ids != set():
        raise ValueError("new_ids are not a subset of old_ids")

    for ge in galaxy_cluster.galaxy_elements:
        if ge.id in to_delete:
            await db.delete(ge)
        else:
            ge.patch(**maybe_updated_dict[ge.id])

    for ge_dict in added_dict:
        db.add(GalaxyElement(galaxy_cluster_id=galaxy_cluster.id, **ge_dict.dict(exclude_none=True)))
