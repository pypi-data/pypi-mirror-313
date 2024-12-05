import logging, psutil, sys, subprocess, platform

from etiket_client.settings.user_settings import user_settings
from typing import List

logger = logging.getLogger(__name__)

DETACHED_PROCESS = 0x00000008
CREATE_NEW_PROCESS_GROUP = 0x00000200

def start_sync_agent():
    logger.info('Trying to start a new sync agent.')
    name ='etiket_sync'
    module_name =  'etiket_client.sync.run'
    cmd = [sys.executable, '-m', module_name, '--detached' ]
    
    running, procs = _is_running(name , module_name, use_settings=False)
    if not running:
        if platform.system() == 'Windows':
            creationflags = DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP
        else:
            creationflags = 0
        proc = subprocess.Popen(
                cmd,
                creationflags=creationflags,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                close_fds=True,
                text=True)
        logger.info('New sync process started.')
    else:
        proc = procs[0]
    
    user_settings.sync_PID = proc.pid
    user_settings.write()

def restart_sync_agent():
    logger.info('Trying to restart the sync agent.')
    kill_sync_agent()
    start_sync_agent()

def is_running_sync_agent(fast = True):
    name ='etiket_sync'
    module_name =  'etiket_client.sync.run'
    running, _ = _is_running(name, module_name, use_settings=fast)
    return running

def kill_sync_agent():
    name ='etiket_sync'
    module_name =  'etiket_client.sync.run'
    running, procs = _is_running(name, module_name, use_settings=False)
    if running:
        for proc in procs: proc.kill()
                    
def _is_running(name, module_name, use_settings=True) -> 'List[bool, List[psutil.Process]]':
    logger.info('Checking if sync agent is running, use_settings = %s.', use_settings)

    if use_settings:
        user_settings.load()
        if user_settings.sync_PID:
            try:
                proc = psutil.Process(user_settings.sync_PID)
                if proc.name().startswith('python') or proc.name().startswith('Python'):
                    if module_name in proc.cmdline() or 'Python qdrive sync' in proc.cmdline():
                        logger.info('Sync agent is running (proc name :: %s, with module name : %s and PID %s).', name, module_name, proc.pid)
                        return True, [proc]
            except (psutil.AccessDenied, psutil.ZombieProcess, psutil.NoSuchProcess):
                pass
    else:
        procs = []
        for proc in psutil.process_iter(['name', 'cmdline', 'pid']):
            try:
                if proc.name().startswith('python') or proc.name().startswith('Python'):
                    if module_name in proc.cmdline() or 'Python qdrive sync' in proc.cmdline():
                        logger.info('Sync agent is running (proc name :: %s, with module name : %s and PID %s).', name, module_name, proc.pid)
                        procs.append(proc)
            except (psutil.AccessDenied, psutil.ZombieProcess, psutil.NoSuchProcess):
                continue
        if procs: return True, procs

    logger.info('No sync agent is active.')
    return False, []