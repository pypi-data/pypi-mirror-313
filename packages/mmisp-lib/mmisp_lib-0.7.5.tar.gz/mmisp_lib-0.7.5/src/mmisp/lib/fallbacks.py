from mmisp.db.models.organisation import Organisation

GENERIC_MISP_ORGANISATION = Organisation(
    id="0",
    name="MISP",
    date_created=None,
    date_modified=None,
    description="Automatically generated MISP organisation",
    type="",
    nationality="Not specified",
    sector="",
    created_by="0",
    uuid="0",
    contacts="",
    local=True,
    restricted_to_domain=[],
    landingpage=None,
)
