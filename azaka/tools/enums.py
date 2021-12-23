import enum

__all__ = ("VN",)


class VN(enum.Enum):
    id = (">", "==", "!=", ">=", "<", "<=")
