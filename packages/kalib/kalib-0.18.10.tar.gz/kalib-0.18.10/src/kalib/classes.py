from kalib.internals import Nothing


class Singleton(type):

    def __init__(cls, name, parents, attrbutes):
        super().__init__(name, parents, attrbutes)
        cls.instance = Nothing

    def __call__(cls, *args, **kw):
        if cls.instance is Nothing:
            cls.instance = super().__call__(*args, **kw)
        return cls.instance
