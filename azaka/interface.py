from .commands import VNCondition


class Interface:
    def __init__(self, type_):
        if type_ == "VN":
            self.condition = VNCondition

        self._conditions = []

    def __enter__(self):
        return self

    def __exit__(self, *ex):
        ...

    def set_condition(self, item):
        self._conditions.extend(item._exprs)
