from __future__ import annotations

import typing as t
from .proxy import ConditionProxy

if t.TYPE_CHECKING:
    from .proxy import BoolOProxy

__all__ = ("VNCondition", "ReleaseCondition")


class Operator:

    __slots__ = ("symbols",)

    def __init__(self, *symbols: str) -> None:
        self.symbols = symbols

    @classmethod
    def fill_some(cls, *symbols: str) -> Operator:
        return cls("=", "!=", *symbols)

    @classmethod
    def fill_all(cls, *symbols: str) -> Operator:
        return cls("=", "!=", ">", ">=", "<", "<=", *symbols)


class VNCondition:

    ID = ConditionProxy("id", operator=Operator.fill_all())
    ID_ARRAY = ConditionProxy("id", operator=Operator.fill_some())

    TITLE = ConditionProxy("title", operator=Operator.fill_some("~"))

    PLATFORMS = ConditionProxy("platforms", operator=Operator.fill_some())
    PLATFORMS_ARRAY = PLATFORMS

    RELEASED = ConditionProxy("released", operator=Operator.fill_some())
    RELEASED_DATE = ConditionProxy("released", operator=Operator.fill_all())

    LANGUAGES = ConditionProxy("languages", operator=Operator.fill_some())
    LANGUAGES_ARRAY = LANGUAGES

    FIRSTCHAR = ConditionProxy("firstchar", operator=Operator.fill_some())

    ORIG_LANG = ConditionProxy("orig_lang", operator=Operator.fill_some())
    ORIG_LANG_ARRAY = ORIG_LANG

    SEARCH = ConditionProxy("search", operator=Operator("~"))

    TAGS = ConditionProxy("tags", Operator.fill_some())
    TAGS_ARRAY = TAGS

    __slots__ = ("_expr",)

    def __init__(self) -> None:
        self._expr: t.Optional[BoolOProxy] = None

    def put(self, item: BoolOProxy) -> None:
        self._expr = item

    def __getitem__(self, items: BoolOProxy) -> t.Optional[BoolOProxy]:
        self.put(items)
        return self._expr

    def __enter__(self) -> VNCondition:
        return self

    def __exit__(self, *ex) -> None:
        ...


class ReleaseCondition:
    ID = ConditionProxy("id", operator=Operator.fill_all())
    ID_ARRAY = ConditionProxy("id", operator=Operator.fill_some())

    VN = ConditionProxy("vn", operator=Operator.fill_some())
    VN_ARRAY = VN

    PRODUCER = ConditionProxy("producer", operator=Operator("="))
    TITLE = ConditionProxy("title", operator=Operator.fill_some("~"))
    ORIGINAL = ConditionProxy("original", operator=Operator.fill_some("~"))

    RELEASED = ConditionProxy("date", operator=Operator.fill_some())
    RELEASED_DATE = ConditionProxy("date", operator=Operator.fill_all())

    PATCH = ConditionProxy("patch", operator=Operator.fill_some("="))
    FREEWARE = ConditionProxy("freeware", operator=Operator.fill_some("="))
    DOUJIN = ConditionProxy("doujin", operator=Operator.fill_some("="))

    TYPE = ConditionProxy("type", operator=Operator.fill_some())
    GTIN = ConditionProxy("gtin", operator=Operator.fill_some())
    CATALOG = ConditionProxy("catalog", operator=Operator.fill_some())

    LANGUAGES = ConditionProxy("languages", operator=Operator.fill_some())
    LANGUAGES_ARRAY = LANGUAGES

    PLATFORMS = ConditionProxy("platforms", operator=Operator.fill_some())
    PLATFORMS_ARRAY = PLATFORMS

    def __init__(self) -> None:
        self._expr: t.Optional[BoolOProxy] = None

    def put(self, item: BoolOProxy) -> None:
        self._expr = item

    def __getitem__(self, items: BoolOProxy) -> t.Optional[BoolOProxy]:
        self.put(items)
        return self._expr

    def __enter__(self) -> ReleaseCondition:
        return self

    def __exit__(self, *ex) -> None:
        ...
