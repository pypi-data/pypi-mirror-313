import fire
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from mmisp.db.models.organisation import Organisation
from mmisp.db.models.user import User

organisation_fields = []


async def create(
    session: AsyncSession,
    name: str,
    admin_email: int | str | None,
    description: str | None,
    type: str | None,
    nationality: str | None,
    sector: str | None,
    contacts_email: str | None,
    local: bool | None,
    restricted_domain: str | None,
    landingpage: str | None,
) -> None:
    organisation = Organisation()

    if await check_if_organisation_exists(session, name):
        raise fire.core.FireError("Organisation with name already exists")

    await set_attributes(
        session,
        organisation,
        name,
        admin_email,
        description,
        type,
        nationality,
        sector,
        contacts_email,
        local,
        restricted_domain,
        landingpage,
    )
    session.add(organisation)
    await session.commit()


async def check_if_organisation_exists(session: AsyncSession, name: str | int) -> bool:
    if isinstance(name, str):
        query = select(Organisation).where(Organisation.name == name)
    else:
        query = select(Organisation).where(Organisation.id == name)
    organisation = await session.execute(query)
    organisation = organisation.scalar_one_or_none()
    if organisation is None:
        return False
    return True


async def edit_organisation(
    session: AsyncSession,
    organisation: str | int,
    new_name: str | None,
    admin_email: int | str | None,
    description: str | None,
    type: str | None,
    nationality: str | None,
    sector: str | None,
    contacts_email: str | None,
    local: bool | None,
    restricted_domain: str | None,
    landingpage: str | None,
) -> None:
    if isinstance(organisation, str):
        query = select(Organisation).where(Organisation.name == organisation)
    else:
        query = select(Organisation).where(Organisation.id == organisation)
    organisation = await session.execute(query)
    organisation = organisation.scalar_one_or_none()

    if organisation is None:
        raise fire.core.FireError("Organisation does not exist")

    await set_attributes(
        session,
        organisation,
        new_name,
        admin_email,
        description,
        type,
        nationality,
        sector,
        contacts_email,
        local,
        restricted_domain,
        landingpage,
    )

    await session.commit()


async def set_attributes(
    session: AsyncSession,
    organisation: Organisation,
    name: str | None,
    admin_user: int | str | None,
    description: str | None,
    type: str | None,
    nationality: str | None,
    sector: str | None,
    contacts_email: str | None,
    local: bool | None,
    restricted_domain: str | None,
    landingpage: str | None,
) -> None:
    if name is not None:
        organisation.name = name
    if admin_user is not None:
        if isinstance(admin_user, str):
            admin_user = await session.execute(select(User).where(User.email == admin_user))
        else:
            admin_user = await session.execute(select(User).where(User.id == admin_user))

        admin_user = admin_user.scalar_one_or_none()
        if admin_user is None:
            raise fire.core.FireError("User does not exist")
        organisation.created_by = admin_user.id
    if description is not None:
        organisation.description = description
    if type is not None:
        organisation.type = type
    if nationality is not None:
        organisation.nationality = nationality
    if sector is not None:
        organisation.sector = sector
    if contacts_email is not None:
        organisation.contacts = contacts_email
    if local is not None:
        organisation.local = local
    if restricted_domain is not None:
        organisation.restricted_to_domain = restricted_domain
    if landingpage is not None:
        organisation.landingpage = landingpage


async def delete_organisation(session: AsyncSession, organisation: str | int) -> None:
    if isinstance(organisation, str):
        query = select(Organisation).where(Organisation.name == organisation)
    else:
        query = select(Organisation).where(Organisation.id == organisation)
    organisation = await session.execute(query)
    organisation = organisation.scalar_one_or_none()

    if organisation is None:
        raise fire.core.FireError("Organisation does not exist")

    await session.delete(organisation)
    await session.commit()
