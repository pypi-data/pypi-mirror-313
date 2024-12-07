import base64
from binascii import Error
from collections import deque
from contextlib import suppress
from pickle import UnpicklingError
from pickle import dumps as generic_dumps
from pickle import loads as generic_loads
from typing import ClassVar

from kalib._internal import to_ascii, to_bytes
from kalib.importer import required
from kalib.internals import (
    Nothing,
    Who,
    class_of,
    is_collection,
    is_function,
    is_mapping,
    sourcefile,
)
from kalib.loggers import Logging
from kalib.monkey import Monkey
from kalib.text import Str

BACKENDS = {b'json': 'orjson', b'ujson': 'orjson'}
DEADBEEF = b'\xDE\xAD\xBE\xEF'

serializers = {}
logger = Logging.get(__name__)


try:
    json = required(BACKENDS[b'json'])

    from orjson import (
        OPT_INDENT_2,
        OPT_NAIVE_UTC,
        OPT_NON_STR_KEYS,
        OPT_SERIALIZE_DATACLASS,
        OPT_SERIALIZE_NUMPY,
        OPT_SERIALIZE_UUID,
        OPT_SORT_KEYS,
        OPT_STRICT_INTEGER,
        JSONDecodeError,
    )

    OPT_JSON_FLAGS = (
        OPT_NAIVE_UTC |
        OPT_NON_STR_KEYS |
        OPT_SERIALIZE_DATACLASS |
        OPT_SERIALIZE_NUMPY |
        OPT_SERIALIZE_UUID |
        OPT_SORT_KEYS |
        OPT_STRICT_INTEGER)

except ImportError:
    import json
    OPT_JSON_FLAGS = None


try:
    CompressorException = required('zstd.Error')
    from zstd import compress, decompress

except ImportError:
    from gzip import BadGzipFile as CompressorException
    from gzip import compress, decompress


try:
    EncoderException = required('base2048.DecodeError', quiet=True)
    import base2048

except ImportError:
    EncoderException = ValueError



class SerializeError(Exception):
    ...


def default_serializer(obj, throw=True):

    if obj is Nothing:
        return None

    if (
        isinstance(obj, tuple) and
        type(obj).__mro__ == (type(obj), tuple, object)
    ):
        return {f'<{type(obj).__name__}>': obj._asdict()}

    with suppress(KeyError):
        result = serializers[class_of(obj)](obj)
        if result is not Nothing:
            return result

    for types, callback in serializers.items():
        if isinstance(obj, types):
            result = callback(obj)
            if result is not Nothing:
                return result

    if throw:
        msg = f"couldn't serialize {Who.Is(obj)}"
        raise TypeError(msg)

    return Nothing


def serializer(*classes):

    direct_call = len(classes) == 2 and is_function(classes[1])  # noqa: PLR2004

    def name(obj):
        return f'{Who(obj, addr=True)} ({sourcefile(obj)})'

    def serialize(func):

        order = [classes[0]] if direct_call else classes
        for cls in order:

            if isinstance(cls, bytes | str):
                cls = required(cls)  # noqa: PLW2901

            if cls in serializers:
                logger.warning(
                    f'{Who(cls)} already have registered serializer '
                    f"{name(serializers[cls])}, can't add another "
                    f'{name(func)}', trace=True, shift=-1)
                continue
            serializers[cls] = func

        title = Who(func)
        msg = f'{", ".join(map(Who, order))}'
        if not (direct_call or title.endswith('.<lambda>')):
            msg = f'{msg} -> {title}'

        logger.verbose(msg)
        return func

    if direct_call:
        return serialize(classes[1])
    else:
        return serialize


@Monkey.wrap(json, 'dumps')
def to_json(func, data, /, **kw):

    minify = kw.pop('minify', True)
    option = kw.pop('option', Nothing)

    if OPT_JSON_FLAGS:
        # enabled only when orjson used and imported
        flags = (option or (0x0 if minify else OPT_INDENT_2))
        kw['option'] = OPT_JSON_FLAGS | flags

    elif option is not Nothing:
        # intercept orjson option when orjson not available
        logger.warning(
            f'{option=} passed, but is not supported by '
            f'stdlib json, install orjson', trace=True)

    elif not minify:
        # stdlib json with indent option
        kw.setdefault('indent', 2)
        kw.setdefault('sort_keys', True)

    kw.setdefault('default', default_serializer)
    encode = (to_ascii, to_bytes)[bool(kw.pop('bytes', False))]
    return encode(func(data, **kw))


if OPT_JSON_FLAGS:
    json.JSONDecodeError = JSONDecodeError


@Monkey.bind(json, 'repr')
def try_json(data, /, **kw):
    with suppress(Exception):
        if hasattr(data, 'as_json'):
            return data.as_json

        elif hasattr(data, 'as_dict'):
            return to_json(data.as_dict, **kw)

    try:
        return to_json(data, **kw)

    except Exception:  # noqa: BLE001
        return repr(data)


@Monkey.bind(json)
def cast(obj):

    if is_mapping(obj):
        return {k: cast(v) for k, v in obj.items()}

    elif isinstance(obj, tuple) and hasattr(obj, '_fields'):  # namedtuple
        return cast(obj._asdict())

    elif isinstance(obj, deque | list | tuple | set):
        return list(map(cast, obj))

    elif is_collection(obj):
        msg = f"couldn't serialize {Who.Is(obj)}"
        raise TypeError(msg)

    result = default_serializer(obj, throw=False)
    return obj if result is Nothing else result


class Encoding:
    Base16   = base64.b16encode, base64.b16decode, 'ascii'
    Base32   = base64.b32encode, base64.b32decode, 'ascii'
    Base64   = base64.b64encode, base64.b64decode, 'ascii'
    Base85   = base64.b85encode, base64.b85decode, 'ascii'
    Codecs = [Base16, Base32, Base64, Base85]  # noqa: RUF012

    if EncoderException is not ValueError:
        Base2048 = base2048.encode, base2048.decode, 'utf-8'
        Codecs.append(Base2048)

    Last = Codecs[-1]
    Codecs = tuple(Codecs)

    Charsets: ClassVar[dict[str, tuple]] = {
        '0123456789ABCDEF': Base16,
        '234567=ABCDEFGHIJKLMNOPQRSTUVWXYZ': Base32,
        '+/0123456789=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz': Base64,
        (
            '!#$%&()*+-0123456789;<=>?@ABCDEFGHIJKLMNOPQ'
            'RSTUVWXYZ^_`abcdefghijklmnopqrstuvwxyz{|}~'
        ): Base85,
    }


def dumps(value, /, encoder=None, proto=None, ratio=None, charset=None):
    """Pickle & compress any object with any pickler with .dumps/loads methods
    and store module name with value for automatic unpickling."""

    if encoder is None:
        value = generic_dumps(value, proto or -1)

    else:
        encoder = to_bytes(encoder)
        if len(encoder) >= 32 - len(DEADBEEF):
            msg = (
                f'len({encoder=})={len(encoder):d} '
                f'must be lower than {32 - len(DEADBEEF):d}')
            raise ValueError(msg)

        module = required(BACKENDS.get(encoder) or encoder)
        value = module.dumps(value)
        value = encoder + DEADBEEF + to_bytes(value, charset=charset or 'utf-8')

    return compress(value, ratio or 9)


def loads(value, /, expect=None):
    """Decompress pickled by dumps function objects with autodetect used module
    for marshallization.

    by default, expecting four exceptions for back compatibility with
    default dumb cache and pass all errors from cache
    """

    if value is None:
        return

    if expect is None:
        expect = TypeError, ValueError, UnpicklingError, CompressorException

    try:
        value = decompress(value)

    except expect:
        with suppress(Exception):
            return json.loads(value)
        return

    offset = value[:32].find(DEADBEEF)
    if offset != -1:
        encoder = to_bytes(value[:offset])
        return (
            required(BACKENDS.get(encoder) or encoder)
            .loads(value[offset + len(DEADBEEF):]))

    with suppress(expect):
        return generic_loads(value)  # noqa: S301


def pack(value, *args, codec=Encoding.Last, **kw):
    return (
        bytes(hex(Encoding.Codecs.index(codec)), 'ascii')[2:] +
        Str.to_bytes(codec[0](to_bytes(dumps(value, *args, **kw))), codec[2])
    ).decode(codec[2])


def unpack(string, *args, **kw):
    last = kw.pop('last', False)
    try:
        codec = Encoding.Codecs[int(string[0])][1]
        return loads(codec(string[1:]), *args, **kw)

    except (IndexError, ValueError, Error):
        if last:
            return

        with suppress(EncoderException, ValueError, Error):
            for charset in reversed(Encoding.Charsets):
                codec = Encoding.Codecs.index(Encoding.Charsets[charset])
                result = unpack(string.__class__(codec) + string, last=True)
                if result:
                    return result

            codec = Encoding.Codecs.index(Encoding.Last)
            result = unpack(string.__class__(codec) + string, last=True)
            if result:
                return result

        return loads(string, *args, **kw)
