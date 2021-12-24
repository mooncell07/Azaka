from __future__ import annotations

import typing as t
from .proxy import ConditionProxy

if t.TYPE_CHECKING:
    from .proxy import BoolOProxy

__all__ = ("VNCondition",)


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
    def __init__(self) -> None:

        self._exprs: t.List[BoolOProxy] = []

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

    def put(self, item: t.Union[t.Tuple[BoolOProxy], BoolOProxy]) -> None:
        if isinstance(item, tuple):
            self._exprs.extend(item)
        else:
            self._exprs.append(item)

    def __getitem__(self, items: t.Union[t.Tuple[BoolOProxy], BoolOProxy]) -> None:
        self.put(items)

    def __enter__(self) -> VNCondition:
        return self

    def __exit__(self, *ex) -> None:
        ...
