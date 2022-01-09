import enum

__all__ = (
    "Flags",
    "ResponseType",
    "ErrorType",
    "Gender",
    "Spoiler",
    "Roles",
    "VoicedType",
    "AnimationType",
    "Rtype",
)


class Flags(enum.Enum):
    """
    An [enum.Enum][] of all the available flags.

    Attributes:
        BASIC: The `basic` flag.
        DETAILSl The `details` flag.
        ANIME: The `anime` flag.
        RELATIONS: The `relations` flag.
        TAGS: The `tags` flag.
        STATS: The `stats` flag.
        SCREENS: The `screens` flag.
        STAFF: The `staff` flag.
        VN: The `vn` flag.
        PRODUCERS: The `producers` flag.
        MEAS: The `meas` flag.
        TRAITS: The `traits` flag.
        VNS: The `vns` flag.
        VOICED: The `voiced` flag.
        INSTANCES: The `instances` flag.
        ALIASES: The `aliases`flag.
        LABELS: The `labels` flag.
    """

    BASIC: str = "basic"
    DETAILS: str = "details"
    ANIME: str = "anime"
    RELATIONS: str = "relations"
    TAGS: str = "tags"
    STATS: str = "stats"
    SCREENS: str = "screens"
    STAFF: str = "staff"
    VN: str = "vn"
    PRODUCERS: str = "producers"
    MEAS: str = "meas"
    TRAITS: str = "traits"
    VNS: str = "vns"
    VOICED: str = "voiced"
    INSTANCES: str = "instances"
    ALIASES: str = "aliases"
    LABELS: str = "labels"


class ResponseType(enum.Enum):
    """
    An [enum.Enum][] of all the available response types.

    Attributes:
        OK: The `ok` response type.
        ERROR: The `error` response type.
        DBSTATS: The `dbstats` response type.
        SESSION: The `session` response type.
        RESULTS: The `results` response type.
    """

    OK: str = "ok"
    RESULTS: str = "results"
    SESSION: str = "session"
    DBSTATS: str = "dbstats"
    ERROR: str = "error"


class ErrorType(enum.Enum):
    """
    An [enum.Enum][] of all the available error types.

    Attributes:
        PARSE: The `parse` error type.
        MISSING: The `missing` error type.
        BADARG: The `badarg` error type.
        NEEDLOGIN: The `needlogin` error type.
        THROTTLED: The `throttled` error type.
        AUTH: The `auth` error type.
        LOGGEDIN: The `loggedin` error type.
        GETTYPE: The `gettype` error type.
        SETTYPE: The `settype` error type.
        FILTER: The `filter` error type.
        GETINFO: The `getinfo` error type.
    """

    PARSE: str = "parse"
    MISSING: str = "missing"
    BADARG: str = "badarg"
    NEEDLOGIN: str = "needlogin"
    THROTTLED: str = "throttled"
    AUTH: str = "auth"
    LOGGEDIN: str = "loggedin"
    GETTYPE: str = "gettype"
    GETINFO: str = "getinfo"
    FILTER: str = "filter"
    SETTYPE: str = "settype"


class Gender(enum.Enum):
    """
    An [enum.Enum][] of all available genders.

    Attributes:
        MALE: The `m` (male) Gender.
        FEMALE: The `f` (female) Gender.
        BOTH: The `b` (??)
    """

    MALE: str = "m"
    FEMALE: str = "f"
    BOTH: str = "b"


class Rtype(enum.Enum):
    """
    An [enum.Enum][] of all available release type (rtype).

    Attributes:
        TRIAL: The `trial` rtype.
        PARTIAL: The `partial` rtype.
        COMPLETE: The `complete` rtype.
    """

    TRIAL: str = "trial"
    PARTIAL: str = "partial"
    COMPLETE: str = "complete"


class Roles(enum.Enum):
    MAIN = "main"
    PRIMARY = "primary"
    SIDE = "side"
    APPEARS = "appears"


class Spoiler(enum.IntEnum):
    NONE = 0
    MINOR = 1
    MAJOR = 2


class VoicedType(enum.IntEnum):
    NOT_VOICED = 1
    ONLY_ERO_VOICED = 2
    PARTIALLY_VOICED = 3
    FULLY_VOICED = 4


class AnimationType(enum.IntEnum):
    NO_ANIMATIONS = 1
    SIMPLE_ANIMATIONS = 2
    PARTIAL_ANIMATIONS = 3
    FULL_ANIMATIONS = 4
