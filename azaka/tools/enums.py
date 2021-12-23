import enum

__all__ = ("VN",)


class Operator:
    def __init__(self, *symbols) -> None:
        self.symbols = symbols

    @classmethod
    def fill_some(cls, *symbols):
        return cls("=", "!=", *symbols)

    @classmethod
    def fill_all(cls, *symbols):
        return cls("=", "!=", ">", ">=", "<", "<=", *symbols)


class VN(enum.Enum):
    title = Operator.fill_some("~")
    original = Operator.fill_some("~")
    firstchar = Operator.fill_some()

    id = Operator.fill_all()
    id_ex = Operator.fill_some()

    platforms = Operator.fill_some()

    released = Operator.fill_some()
    released_ex = Operator.fill_all()

    languages = Operator.fill_some()
    orig_lang = Operator.fill_some()

    search = Operator("~")
