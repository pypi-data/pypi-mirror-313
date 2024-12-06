import contextlib
import copy
import logging
import os

log = logging.getLogger(__name__)


@contextlib.contextmanager
def env_var_context(**kwargs):
    # must use copy.deepcopy, else old_env will be shallow reference to
    # os.environ & will reflect changes made to it
    old_env = copy.deepcopy(os.environ)
    # env vars' keys & values can only be strings
    # key we don't have to worry about; **kwargs keys can only be strings
    for k in kwargs.keys():
        # may raise TypeError if value cannot be stringified
        kwargs[k] = str(kwargs[k])
    try:
        os.environ.update(kwargs)
        log.debug(f"added to os.environ: {kwargs}")
        yield
    finally:
        os.environ = old_env

