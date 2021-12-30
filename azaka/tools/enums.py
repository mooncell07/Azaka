import enum

__all__ = ("Type", "Flags", "ResponseType", "ErrorType")


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
