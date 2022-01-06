import enum

__all__ = ("Type", "Flags", "ResponseType", "ErrorType", "Gender", "Spoiler", "Roles")


class Type(enum.Enum):
    VN = "vn"
    RELEASE = "release"
    PRODUCER = "producer"
    CHARACTER = "character"
    STAFF = "staff"
    QUOTE = "quote"
    USER = "user"
    ULIST_LABELS = "ulist-labels"
    ULIST = "ulist"


class Flags(enum.Enum):
    BASIC = "basic"
    DETAILS = "details"
    ANIME = "anime"
    RELATIONS = "relations"
    TAGS = "tags"
    STATS = "stats"
    SCREENS = "screens"
    STAFF = "staff"
    VN = "vn"
    PRODUCERS = "producers"
    MEAS = "meas"
    TRAITS = "traits"
    VNS = "vns"
    VOICED = "voiced"
    INSTANCES = "instances"
    ALIASES = "aliases"
    LABELS = "labels"


class ResponseType(enum.Enum):
    OK = "ok"
    RESULTS = "results"
    SESSION = "session"
    DBSTATS = "dbstats"
    ERROR = "error"


class ErrorType(enum.Enum):
    PARSE = "parse"
    MISSING = "missing"
    BADARG = "badarg"
    NEEDLOGIN = "needlogin"
    THROTTLED = "throttled"
    AUTH = "auth"
    LOGGEDIN = "loggedin"
    GETTYPE = "gettype"
    GETINFO = "getinfo"
    FILTER = "filter"
    SETTYPE = "settype"


class Gender(enum.Enum):
    MALE = "m"
    FEMALE = "f"
    BOTH = "b"


class Spoiler(enum.IntEnum):
    NONE = 0
    MINOR = 1
    MAJOR = 2


class Roles(enum.Enum):
    MAIN = "main"
    PRIMARY = "primary"
    SIDE = "side"
    APPEARS = "appears"
