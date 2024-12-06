import logging
import os

log = logging.getLogger(__name__)

PROJECT_ROOT = os.path.realpath(os.path.dirname(os.path.dirname(__file__))) 
ETC_PATH = os.path.sep.join([PROJECT_ROOT, 'etc'])

def get_env_var(var_name, required=True):
    val = ""
    try:
        val = os.environ[var_name]
    except KeyError:
        log.warning(f"{var_name} not found in {sorted(os.environ.keys())}")
        if required:
            raise RuntimeError(f"Please set {var_name}")
    return val

