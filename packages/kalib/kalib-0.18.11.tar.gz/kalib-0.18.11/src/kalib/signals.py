import sys
import time
from pathlib import Path
from signal import signal as bind

from kalib.descriptors import cache
from kalib.loggers import Logging

Logger = Logging.Default
NeedRestart = False


@cache
def get_selfpath():
    return Path(sys.argv[0]).resolve()


def get_mtime():
    return get_selfpath().stat().st_mtime


@cache
def quit_at(*, func=sys.exit, signal=None, errno=137, **kw):

    def handler(signum, frame):  # noqa: ARG001
        global NeedRestart  # noqa: PLW0603
        NeedRestart = True
        Logger.warning(f'{signal=} received, mark restart as needed')

    if signal:
        bind(signal, handler)

    initial_stamp = get_mtime()
    def on_change(*, sleep=0.0):

        if NeedRestart and signal:
            Logger.warning(f'{signal=} received, quit..')
            func(errno)
            return False

        elif initial_stamp != (ctime := get_mtime()):
            file = get_selfpath()
            Logger.warning(
                f'{file=} updated {time.time() - ctime:.2f} seconds ago, quit..')
            func(errno)
            return False

        if sleep := (sleep or kw.get('sleep', 0.0)):
            time.sleep(sleep)
        return True
    return on_change
