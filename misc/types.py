from dataclasses import dataclass


class MetaInner(type):
    def __new__(mcs, name, bases, attrs):
        for attr_name, attr_value in attrs.items():
            if isinstance(attr_value, _Inner):
                attr_value.name = f"{name}~{attr_name}"
        return super().__new__(mcs, name, bases, attrs)

    def __call__(cls, *args):
        if not args:
            return cls.__name__
        else:
            return super().__call__(*args)


class _Inner:
    def __init__(self):
        self.name = None

    def __call__(self, *args):
        if not args:
            return self.name
        args = map(str, args) 
        return f"{self.name}~{'~'.join(args)}"


@dataclass
class CallbackExtract:
    data: str
    args: list


class CallbackData:
    class Admin(metaclass=MetaInner):
        hello = _Inner()
        ross = _Inner()
        get_admins = _Inner()
        get_db = _Inner()
        remove_admin = _Inner()
        move_admins = _Inner()
        main = _Inner()
        confirm_ross = _Inner()

    class Start(metaclass=MetaInner):
        bots = _Inner()

    class Back(metaclass=MetaInner):
        main_menu = _Inner()

    class Bots(metaclass=MetaInner):
        move = _Inner()
        new = _Inner()
        remove = _Inner()
        select = _Inner()

    @staticmethod
    def extract(data: str) -> CallbackExtract:
        _data = "~".join(data.split("~")[:2])
        args = data.split("~")[2:] if len(data.split("~")) > 2 else None
        return CallbackExtract(data=_data, args=args)
