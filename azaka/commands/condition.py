from .proxy import ConditionProxy

__all__ = ("VNCondition",)


class Operator:

    __slots__ = ("symbols",)

    def __init__(self, *symbols) -> None:
        self.symbols = symbols

    @classmethod
    def fill_some(cls, *symbols):
        return cls("=", "!=", *symbols)

    @classmethod
    def fill_all(cls, *symbols):
        return cls("=", "!=", ">", ">=", "<", "<=", *symbols)


class VNCondition:
    def __init__(self) -> None:

        self._exprs = []

        self.id = ConditionProxy("id", operator=Operator.fill_all())
        self.id_array = ConditionProxy("id", operator=Operator.fill_some())

        self.title = ConditionProxy("title", operator=Operator.fill_some("~"))

        self.platforms = ConditionProxy("platforms", operator=Operator.fill_some())
        self.platforms_array = self.platforms

        self.released = ConditionProxy("released", operator=Operator.fill_some())
        self.released_date = ConditionProxy("released", operator=Operator.fill_all())

        self.languages = ConditionProxy("languages", operator=Operator.fill_some())
        self.languages_array = self.languages

        self.firstchar = ConditionProxy("firstchar", operator=Operator.fill_some())

        self.orig_lang = ConditionProxy("orig_lang", operator=Operator.fill_some())
        self.orig_lang_array = self.orig_lang

        self.search = ConditionProxy("search", operator=Operator("~"))

    def put(self, item):
        try:
            self._exprs.extend(item)
        except TypeError:
            self._exprs.append(item)
        return item

    def __getitem__(self, items):
        self.put(items)

    def __enter__(self):
        return self

    def __exit__(self, *ex):
        ...
