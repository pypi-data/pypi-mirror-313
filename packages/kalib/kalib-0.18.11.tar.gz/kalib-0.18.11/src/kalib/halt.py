import sys

from kalib.loggers import Logging

Logging.get(__name__).exception('halt', trace=True, shift=-2, stack=2)
sys.exit(127)
