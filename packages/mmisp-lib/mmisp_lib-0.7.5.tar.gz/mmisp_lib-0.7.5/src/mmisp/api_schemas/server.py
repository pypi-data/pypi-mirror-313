from pydantic import BaseModel

from mmisp.api_schemas.organisations import ServerOrganisation
from mmisp.api_schemas.users import ServerUser


class ServerVersion(BaseModel):
    version: str
    pymisp_recommended_version: str
    perm_sync: bool
    perm_sighting: bool
    perm_galaxy_editor: bool
    perm_analyst_data: bool
    uuid: str
    request_encoding: list[str]
    filter_sightings: bool


class Server(BaseModel):
    id: int
    name: str
    url: str
    org_id: int
    push: bool
    pull: bool
    push_sightings: bool
    push_galaxy_clusters: bool
    push_analyst_data: bool
    pull_analyst_data: bool
    pull_galaxy_clusters: bool
    lastpulledid: int | None = None
    lastpushedid: int | None = None
    organization: str | None = None
    remote_org_id: int
    publish_without_email: bool
    unpublish_event: bool
    self_signed: bool
    pull_rules: str
    push_rules: str
    cert_file: str | None = None
    client_cert_file: str | None = None
    internal: bool
    skip_proxy: bool
    remove_missing_tags: bool
    caching_enabled: bool
    priority: int | None = None
    cache_timestamp: bool


class ServerViewMeResponse(BaseModel):
    Server: Server
    Organisation: ServerOrganisation
    RemotesOrg: ServerOrganisation
    User: ServerUser
