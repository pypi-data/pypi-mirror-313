from etiket_client.local.dao.user import dao_user, UserCreate, UserUpdate, UserDoesNotExistException
from etiket_client.remote.endpoints.user import user_read_me

from sqlalchemy.orm import Session

import logging

logger = logging.getLogger(__name__)


def sync_current_user(session : Session):
    user = user_read_me()
    try:
        dao_user.read(user.username, False, session)
        userupdate = UserUpdate(firstname=user.firstname, lastname=user.lastname,
                                email=user.email, user_type=user.user_type, active=user.active, disable_on=user.disable_on)
        dao_user.update(user.username, userupdate, session)
    except UserDoesNotExistException:
        uc = UserCreate(username=user.username, firstname=user.firstname, lastname=user.lastname,
                                email=user.email, active = user.active,  user_type=user.user_type, disable_on=user.disable_on)
        dao_user.create(uc, session)
    except Exception as e:
        logger.exception('Error while synchronizing user :: %s', uc.username)
        raise e