from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from mmisp.db.models.organisation import Organisation
from mmisp.db.models.role import Role


async def setup(session: AsyncSession) -> None:
    user = Role()
    user.name = "user"
    await add_role_if_not_exist(session, user)

    admin = Role(
        name="admin",
        perm_add=True,
        perm_modify=True,
        perm_modify_org=True,
        perm_publish=True,
        perm_delegate=True,
        perm_sync=False,
        perm_admin=True,
        perm_audit=True,
        perm_auth=True,
        perm_site_admin=False,
        perm_regexp_access=False,
        perm_tagger=True,
        perm_template=True,
        perm_sharing_group=True,
        perm_tag_editor=True,
        perm_sighting=True,
        perm_object_template=False,
        default_role=False,
        memory_limit="",
        max_execution_time="",
        restricted_to_site_admin=False,
        perm_publish_zmq=True,
        perm_publish_kafka=True,
        perm_decaying=True,
        enforce_rate_limit=False,
        rate_limit_count=0,
        perm_galaxy_editor=True,
        perm_warninglist=False,
        perm_view_feed_correlations=True,
    )
    await add_role_if_not_exist(session, admin)

    site_admin = Role(
        name="site_admin",
        perm_add=True,
        perm_modify_org=True,
        perm_publish=True,
        perm_modify=True,
        perm_delegate=True,
        perm_sync=True,
        perm_admin=True,
        perm_audit=True,
        perm_auth=True,
        perm_site_admin=True,
        perm_regexp_access=True,
        perm_tagger=True,
        perm_template=True,
        perm_sharing_group=True,
        perm_tag_editor=True,
        perm_sighting=True,
        perm_object_template=True,
        default_role=False,
        memory_limit="",
        max_execution_time="",
        restricted_to_site_admin=False,
        perm_publish_zmq=True,
        perm_publish_kafka=True,
        perm_decaying=True,
        enforce_rate_limit=False,
        rate_limit_count=0,
        perm_galaxy_editor=True,
        perm_warninglist=True,
        perm_view_feed_correlations=True,
    )
    await add_role_if_not_exist(session, site_admin)

    ghost_org = Organisation()
    ghost_org.name = "ghost_org"
    await add_organisation_if_not_exist(session, ghost_org)


async def add_role_if_not_exist(session: AsyncSession, role: Role) -> None:
    query = select(Role).where(Role.name == role.name)
    role_db = await session.execute(query)
    role_db = role_db.scalar_one_or_none()
    if role_db is None:
        session.add(role)
        await session.commit()


async def add_organisation_if_not_exist(session: AsyncSession, organisation: Organisation) -> None:
    query = select(Organisation).where(Organisation.name == organisation.name)
    organisation_db = await session.execute(query)
    organisation_db = organisation_db.scalar_one_or_none()
    if organisation_db is None:
        session.add(organisation)
        await session.commit()
