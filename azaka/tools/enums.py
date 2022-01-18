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
    "Labels",
)


class Flags(enum.Enum):
    """
    An [enum.Enum][] of all the available flags.
    These flags decide what data the API should return.

    Attributes:
        BASIC: The `basic` flag.
        DETAILS: The `details` flag.
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

    Info:
        These can be stacked together using a tuple.
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
    These are the possible response types API can return and
    in most cases you will not need to use or get them directly.
    except for [Client.set_ulist](../client#azaka.client.Client.set_ulist).

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
    These are the possible error types API can return.
    These are present as an attribute of all errors which inherit from
    [AzakaException](../public/exceptions.md#azaka.exceptions.AzakaException).

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
    """
    An [enum.Enum][] of all available character roles.

    Attributes:
        MAIN: The `main` role.
        PRIMARY: The `primary` role.
        SIDE: The `side` role.
        APPEARS: The `appears` role.
    """

    MAIN: str = "main"
    PRIMARY: str = "primary"
    SIDE: str = "side"
    APPEARS: str = "appears"


class Spoiler(enum.IntEnum):
    """
    An [enum.IntEnum][] of all available spoiler levels.

    Attributes:
        NONE: The `0` spoiler level.
        MINOR: The `1` spoiler level.
        MAJOR: The `2` spoiler level.
    """

    NONE: int = 0
    MINOR: int = 1
    MAJOR: int = 2


class VoicedType(enum.IntEnum):
    """
    An [enum.IntEnum][] of all available voiced types.

    Attributes:
        NOT_VOICED: The `1` voiced type.
        ONLY_ERO_VOICED: The `2` voiced type.
        PARTIALLY_VOICED: The `3` voiced type.
        FULLY_VOICED: The `4` voiced type.
    """

    NOT_VOICED: int = 1
    ONLY_ERO_VOICED: int = 2
    PARTIALLY_VOICED: int = 3
    FULLY_VOICED: int = 4


class AnimationType(enum.IntEnum):
    """
    An [enum.IntEnum][] of all available animation types.

    Attributes:
        NO_ANIMATIONS: The `1` animation type.
        SIMPLE_ANIMATIONS: The `2` animation type.
        PARTIAL_ANIMATIONS: The `3` animation type.
        FULL_ANIMATIONS: The `4` animation type.
    """

    NO_ANIMATIONS: int = 1
    SIMPLE_ANIMATIONS: int = 2
    PARTIAL_ANIMATIONS: int = 3
    FULL_ANIMATIONS: int = 4


class Labels(enum.IntEnum):
    """
    An [enum.IntEnum][] of all available labels.

    Attributes:
        NOLABEL: The `0` label.
        PLAYING: The `1` label.
        FINISHED: The `2` label.
        STALLED: The `3` label.
        DROPPED: The `4` label.
        WISHLIST: The `5` label.
        BLACKLIST: The `6` label.
    """

    NOLABEL: int = 0
    PLAYING: int = 1
    FINISHED: int = 2
    STALLED: int = 3
    DROPPED: int = 4
    WISHLIST: int = 5
    BLACKLIST: int = 6
