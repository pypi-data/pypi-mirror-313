import contextlib
import io
import logging
import shutil
import sys
import tempfile

log = logging.getLogger(__name__)


@contextlib.contextmanager
def tmpdir(cleanup=True):
    """contextmanager that creates tmpdir, yields path, and rms dir @finally

    if you're testing a broken test & need the tempdir to remain after the
    test runs, pass cleanup=False, but never check in code with that parameter
    """
    path = tempfile.mkdtemp()
    log.debug(f"created tmpdir {path}")
    try:
        yield path
    finally:
        if cleanup:
            log.debug(f"removing {path}")
            shutil.rmtree(path)


@contextlib.contextmanager
def mock_stderr():
    """monkeypatches sys.stderr for duration of context"""
    orig_stderr = sys.stderr
    mock_stderr = io.StringIO()
    try:
        sys.stderr = mock_stderr
        yield sys.stderr
    finally:
        sys.stderr = orig_stderr


@contextlib.contextmanager
def mock_stdout():
    """monkeypatches sys.stdout for duration of context"""
    orig_stdout = sys.stdout
    mock_stdout = io.StringIO()
    try:
        sys.stdout = mock_stdout
        yield sys.stdout
    finally:
        sys.stdout = orig_stdout

