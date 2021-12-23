from .tools import VN, ConditionProxy

__all__ = ("VNCondition",)


class VNCondition:
    def __init__(self) -> None:
        self.id = ConditionProxy(VN.id)
        self.id_array = ConditionProxy(VN.id_array)
        self.title = ConditionProxy(VN.title)
        self.platforms = ConditionProxy(VN.platforms)
        self.released = ConditionProxy(VN.released)
        self.languages = ConditionProxy(VN.languages)

    def __getitem__(self, items):
        return items.expression
