#
#                               README
#
# The logger defined here is intended to be imported into the entrypoint of a
# process; either `app.py`, `wsgi.py`, or possibly a command line script, and
# is intended for one-time configuration of app logging behavior
#
# Almost all code should use the standard python logging interface:
#
#    import logging
#    log = logging.getLogger(__name__)
#    log.info("This message will find its way to the correct handlers")
#
# Which is to say, please do not import the logger defined here, unless you
# are sure you know that it is the right thing to do.
#
import logging
import os

from flask.logging import default_handler

LOG_LEVEL = os.environ.get('LOG_LEVEL', logging.INFO)

def get_flask_logger(name, level=LOG_LEVEL):
    log = logging.getLogger(name)
    log.setLevel(level)
    default_handler.setLevel(level)
    log.addHandler(default_handler)
    log.debug(f'get_flask_logger: logging configured @ level {LOG_LEVEL}')
    return log

