from __future__ import annotations

import typing as t

from .proxy import ConditionProxy

if t.TYPE_CHECKING:
    from ..tools import Type
    from .proxy import BoolOProxy


__all__ = (
    "VNCondition",
    "ReleaseCondition",
    "ProducerCondition",
    "CharacterCondition",
    "StaffCondition",
    "QuoteCondition",
    "UserCondition",
    "UlistLabelsCondition",
    "UlistCondition",
    "_condition_selector",
)


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


class BaseCondition:

    ID = ConditionProxy("id", operator=Operator.fill_all())
    ID_ARRAY = ConditionProxy("id", operator=Operator.fill_some())

    __slots__ = ("_expr",)

    def __init__(self) -> None:
        self._expr: t.Optional[BoolOProxy] = None

    def put(self, item: BoolOProxy) -> None:
        self._expr = item

    def __getitem__(self, items: BoolOProxy) -> t.Optional[BoolOProxy]:
        self.put(items)
        return self._expr

    def __enter__(self) -> BaseCondition:
        return self

    def __exit__(self, *ex) -> None:
        ...


class VNCondition(BaseCondition):
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

    __slots__ = ()


class ReleaseCondition(BaseCondition):
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

    __slots__ = ()


class ProducerCondition(BaseCondition):
    NAME = ConditionProxy("name", operator=Operator.fill_some("~"))
    ORIGINAL = ConditionProxy("original", operator=Operator.fill_some("~"))
    TYPE = ConditionProxy("type", operator=Operator.fill_some())

    LANGUAGE = ConditionProxy("language", operator=Operator.fill_some())
    LANGUAGES_ARRAY = LANGUAGE

    SEARCH = ConditionProxy("search", operator=Operator("~"))

    __slots__ = ()


class CharacterCondition(BaseCondition):
    NAME = ConditionProxy("name", operator=Operator.fill_some("~"))
    ORIGINAL = ConditionProxy("original", operator=Operator.fill_some("~"))
    SEARCH = ConditionProxy("search", operator=Operator("~"))

    VN = ConditionProxy("vn", operator=Operator("="))
    VN_ARRAY = VN

    TRAITS = ConditionProxy("traits", operator=Operator.fill_some())
    TRAITS_ARRAY = TRAITS

    __slots__ = ()


class StaffCondition(BaseCondition):
    AID = ConditionProxy("aid", operator=Operator("="))
    AID_ARRAY = AID

    SEARCH = ConditionProxy("search", operator=Operator("~"))

    __slots__ = ()


class QuoteCondition(BaseCondition):
    __slots__ = ()


class UserCondition(BaseCondition):
    USERNAME = ConditionProxy("username", operator=Operator.fill_some("~"))
    USERNAME_ARRAY = ConditionProxy("username", operator=Operator("="))

    __slots__ = ()


class UlistLabelsCondition:
    UID = ConditionProxy("uid", operator=Operator("="))

    __slots__ = ("_expr",)

    def __init__(self) -> None:
        self._expr: t.Optional[BoolOProxy] = None

    def put(self, item: BoolOProxy) -> None:
        self._expr = item

    def __getitem__(self, items: BoolOProxy) -> t.Optional[BoolOProxy]:
        self.put(items)
        return self._expr

    def __enter__(self) -> UlistLabelsCondition:
        return self

    def __exit__(self, *ex) -> None:
        ...


class UlistCondition(UlistLabelsCondition):
    VN = ConditionProxy("vn", operator=Operator.fill_all())
    VN_ARRAY = ConditionProxy("vn", operator=Operator.fill_some())
    LABEL = ConditionProxy("label", operator=Operator("~"))

    __slots__ = ()


def _condition_selector(
    type: Type,
) -> t.Union[t.Type[BaseCondition], t.Type[UlistLabelsCondition], t.Any]:
    condition_map = {
        "vn": VNCondition,
        "release": ReleaseCondition,
        "producer": ProducerCondition,
        "character": CharacterCondition,
        "staff": StaffCondition,
        "quote": QuoteCondition,
        "user": UserCondition,
        "ulist-labels": UlistLabelsCondition,
        "ulist": UlistCondition,
    }
    return condition_map[type.value]
