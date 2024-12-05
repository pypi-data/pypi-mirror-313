from etiket_client.remote.client import client
from etiket_client.remote.endpoints.models.scope import ScopeReadWithUsers, ScopeCreate, ScopeUpdate

import typing, uuid

def scope_create(scopeCreate : ScopeCreate) -> None:
    client.post("/scope/", json_data=scopeCreate.model_dump(mode="json") )

def scope_update(scope_uuid : uuid.UUID, scopeUpdate : ScopeUpdate) -> None:
    client.patch("/scope/", json_data=scopeUpdate.model_dump(mode="json"), params={"scope_uuid":scope_uuid})

def scope_read(scope_uuid : uuid.UUID) -> ScopeReadWithUsers:
    response = client.get("/scope/", params={"scope_uuid":scope_uuid})
    return ScopeReadWithUsers.model_validate(response)

def scope_read_name(name : str) -> ScopeReadWithUsers:
    response = client.get("/scope/", params={"name":name})
    return ScopeReadWithUsers.model_validate(response)

def scope_read_many(name_query : str = None, offset = 0, limit = None) -> typing.List[ScopeReadWithUsers]:
    response = client.get("/scopes/", params={"name":name_query,
                            "offset": offset, "limit":limit})
    return [ScopeReadWithUsers.model_validate(scope) for scope in response]
