from .tools import VN, ConditionProxy

__all__ = ("VNCondition",)


class VNCondition:
    def __init__(self) -> None:
        self.id = ConditionProxy(VN.id)
        self.id_array = ConditionProxy(VN.id_ex)

        self.title = ConditionProxy(VN.title)

        self.platforms = ConditionProxy(VN.platforms)
        self.platforms_array = self.platforms

        self.released = ConditionProxy(VN.released)
        self.released_date = ConditionProxy(VN.released_ex)

        self.languages = ConditionProxy(VN.languages)
        self.languages_array = self.languages

        self.firstchar = ConditionProxy(VN.firstchar)

        self.orig_lang = ConditionProxy(VN.orig_lang)
        self.orig_lang_array = self.orig_lang

        self.search = ConditionProxy(VN.search)

    def __getitem__(self, items):
        return items.expression
