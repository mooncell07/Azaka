import enum

__all__ = ("VN",)


class Operator:
    def __init__(self, *symbols) -> None:
        self.symbols = symbols


class VN(enum.Enum):
    id = Operator(">", "=", "!=", ">=", "<", "<=")
    id_array = Operator("=", "!=")

    title = Operator("=", "!=", "~")

    platforms = Operator("=", "!=")
    platforms_array = Operator("=", "!=")

    released = Operator("=", "!=", ">", ">=", "<", "<=")

    languages = Operator("=", "!=")
    languages_array = Operator("=", "!=")
