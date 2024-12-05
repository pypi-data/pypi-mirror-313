from etiket_client.local.dao.scope import dao_scope, ScopeReadWithUsers
from etiket_client.local.database import Session

from etiket_client.settings.user_settings import user_settings
from etiket_client.sync.backends.native.sync_scopes import sync_scopes

from typing import List

import uuid

def get_selected_scope() -> ScopeReadWithUsers:
    with Session() as session:
        sync_scopes(session)
        current_scope = dao_scope.read(uuid.UUID(user_settings.current_scope), session)
    return current_scope

def get_scopes() -> List[ScopeReadWithUsers]:
    with Session() as session:
        sync_scopes(session)
        scopes = dao_scope.read_all(username=user_settings.user_sub,
                                    session=session)
    return scopes

def get_scope_by_name(name : str) -> ScopeReadWithUsers:
    with Session() as session:
        sync_scopes(session)
        return dao_scope.read_by_name(name, session)

def get_scope_by_uuid(uuid : uuid.UUID) -> ScopeReadWithUsers:
    with Session() as session:
        sync_scopes(session)
        return dao_scope.read(uuid, session)