import fire

import mmisp.db.all_models  # noqa
from mmisp.commandline_tool import organisation, setup, user
from mmisp.db.database import sessionmanager

# This is a simple command line tool that uses the fire library to create a command line tool for creating users
# and organisations and changing their details.


async def setup_db(create_init_values: bool = True) -> str:
    """setup"""
    sessionmanager.init()
    await sessionmanager.create_all()

    if create_init_values:
        async with sessionmanager.session() as session:
            await setup.setup(session)

    await sessionmanager.close()
    return "Database setup"


async def create_user(email: str, password: str, organisation: str | int, role: int | str = "user") -> str:
    """create-user <email> <password> <organisation> [-r <role>]"""
    sessionmanager.init()
    await sessionmanager.create_all()
    async with sessionmanager.session() as session:
        await user.create(session, email, password, organisation, role)

    await sessionmanager.close()
    return "User created with email: {}, password: {}, in organisation: {}, with role: {}".format(
        email, password, organisation, role
    )


async def create_organisation(
    name: str,
    admin_email: int | str | None = None,
    description: str | None = None,
    type: str | None = None,
    nationality: str | None = None,
    sector: str | None = None,
    contacts_email: str | None = None,
    local: bool | None = None,
    restricted_domain: str | None = None,
    landingpage: str | None = None,
) -> str:
    """create-organisation <name> [-admin_email <admin_email>] [- description <description>] [-type <type>]
    [-nationality <nationality>] [<sector>] [<contacts_email>] [-local <local>]
    [- restricted_domain <restricted_domain>] [-landigpage <landingpage>]"""
    sessionmanager.init()
    await sessionmanager.create_all()
    async with sessionmanager.session() as session:
        await organisation.create(
            session,
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

    await sessionmanager.close()

    output = "Organisation created with name: {} admin_email: {} description: {}"
    return output.format(name, admin_email, description)


async def change_password(email: str, password: str) -> str:
    """change-password <email> <password>"""
    sessionmanager.init()
    await sessionmanager.create_all()
    async with sessionmanager.session() as session:
        await user.set_password(session, email, password)

    await sessionmanager.close()
    return "Password changed for user with email: {}".format(email)


async def change_email(email: str, new_email: str) -> str:
    """change-email <email> <new_email>"""
    sessionmanager.init()
    await sessionmanager.create_all()
    async with sessionmanager.session() as session:
        await user.set_email(session, email, new_email)

    await sessionmanager.close()
    return "Email changed for user with email: {} to {}".format(email, new_email)


async def change_role(email: str, role: str | int) -> str:
    """change-role <email> <role>"""
    sessionmanager.init()
    await sessionmanager.create_all()
    async with sessionmanager.session() as session:
        await user.set_role(session, email, role)

    await sessionmanager.close()
    return "Role changed for user with email: {} to {}".format(email, role)


async def edit_organisation(
    org: str | int,
    new_name: str | None = None,
    admin_email: int | str | None = None,
    description: str | None = None,
    type: str | None = None,
    nationality: str | None = None,
    sector: str | None = None,
    contacts_email: str | None = None,
    local: bool | None = None,
    restricted_domain: str | None = None,
    landingpage: str | None = None,
) -> str:
    """edit-organisation <organisation> [-new_name <new_name>] [-admin_email <admin_email>] [-description <description>]
    [-type <type>] [-nationality <nationality>] [-sector <sector>] [-contacts_email <contacts_email>] [-local <local>]
    [-restricted_domain <restricted_domain>] [-landingpage <landingpage>]"""
    output = "organisation {} edited"
    sessionmanager.init()
    await sessionmanager.create_all()

    async with sessionmanager.session() as session:
        await organisation.edit_organisation(
            session,
            org,
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

    await sessionmanager.close()
    return output.format(org)


async def delete_organisation(org: str | int) -> str:
    """delete-organisation <name>"""
    sessionmanager.init()
    await sessionmanager.create_all()
    async with sessionmanager.session() as session:
        await organisation.delete_organisation(session, org)

    await sessionmanager.close()
    return "organisation deleted with name: {}".format(org)


async def delete_user(email: str) -> str:
    """delete-user <email>"""
    sessionmanager.init()
    await sessionmanager.create_all()
    async with sessionmanager.session() as session:
        await user.delete_user(session, email)

    await sessionmanager.close()
    return "User deleted with email: {} ".format(email)


def main() -> None:
    """Main entrypoint for mmisp-db"""
    fire.Fire(
        {
            "setup": setup_db,
            "create-user": create_user,
            "create-organisation": create_organisation,
            "change-password": change_password,
            "change-email": change_email,
            "change-role": change_role,
            "edit-organisation": edit_organisation,
            "delete-organisation": delete_organisation,
            "delete-user": delete_user,
        }
    )


if __name__ == "__main__":
    main()
