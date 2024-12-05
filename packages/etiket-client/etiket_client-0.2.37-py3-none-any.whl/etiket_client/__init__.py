__version__  = '0.2.37'

try:
    from etiket_client.local.dao.app import dao_app_registerer
    from etiket_client.local.types import ProcTypes

    dao_app_registerer.register(__version__, ProcTypes.etiket_client, __file__)
except Exception as e:
    print("Failed to update version information about the current session (etiket_client). \nError: ", e)

from etiket_client.settings.logging import set_up_logging
set_up_logging(__name__, __version__)

from etiket_client.sync.database.start_up import start_up
from etiket_client.sync.proc import start_sync_agent, restart_sync_agent
from etiket_client.remote.authenticate import logout, authenticate_with_console
from etiket_client.misc.update_checker import start_update_checker

start_up()
start_sync_agent()
start_update_checker()