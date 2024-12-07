"""**Integration**:

- The module relies on custom utilities from the `kalib` package, such as:
  - `kalib.datastructures` for JSON handling.
  - `kalib.descriptors` for caching and property management.
  - `kalib.importer` for dynamic imports.
  - `kalib.internals` for introspection utilities.
  - `kalib.loggers` for logging capabilities.
  - `kalib.misc` and `kalib.text` for miscellaneous utilities.

- It integrates with standard Python modules like `dataclass`, `enum`,
`typing`, and `datetime` to provide enhanced functionality while maintaining
compatibility with standard data class features.
"""

from kalib import (
    datastructures,
    descriptors,
    importer,
    internals,
    loggers,
    misc,
    monkey,
    signals,
    text,
    versions,
)
from kalib._internal import to_ascii, to_bytes
from kalib.dataclass import (
    autoclass,
    dataclass,
)
from kalib.datastructures import (
    dumps,
    json,
    loads,
    pack,
    serializer,
    unpack,
)
from kalib.descriptors import (
    cache,
    pin,
    prop,
)
from kalib.exceptions import (
    exception,
)
from kalib.hypertext import (
    HTTP,
    Cookies,
)
from kalib.importer import (
    add_path,
    optional,
    required,
    sort,
)
from kalib.internals import (
    Nothing,
    Who,
    about,
    class_of,
    is_class,
    issubstance,
    sourcefile,
    stacktrace,
    unique,
)
from kalib.loggers import (
    Logging,
    logger,
)
from kalib.misc import (
    Now,
    Partial,
    Timer,
    lazy_proxy_to,
    stamp,
    tty,
)
from kalib.monkey import (
    Monkey,
)
from kalib.signals import (
    quit_at,
)
from kalib.text import (
    Str,
)
from kalib.versions import (
    Git,
    add_versioned_path,
)

__all__ = (
    'HTTP',
    'Cookies',
    'Git',
    'Logging',
    'Monkey',
    'Nothing',
    'Now',
    'Partial',
    'Str',
    'Time',
    'Who',
    'about',
    'add_path',
    'add_versioned_path',
    'autoclass',
    'cache',
    'class_of',
    'dataclass',
    'datastructures',
    'descriptors',
    'dumps',
    'exception',
    'importer',
    'internals',
    'is_class',
    'issubstance',
    'json',
    'lazy_proxy_to',
    'loads',
    'logger',
    'loggers',
    'misc',
    'monkey',
    'optional',
    'pack',
    'pin',
    'prop',
    'quit_at',
    'required',
    'serializer',
    'signals',
    'sort',
    'sourcefile',
    'stacktrace',
    'stamp',
    'text',
    'to_ascii',
    'to_bytes',
    'tty',
    'unique',
    'unpack',
    'versions',
)

Time = Timer()
