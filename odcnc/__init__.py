from functools import update_wrapper


class classproperty(property):
    """
    Decorator that converts a method with a single cls argument into a property
    that can be accessed directly from the class.
    """

    def __get__(self, _, cls=None):
        return self.fget(cls)


class lazyproperty(property):
    def __init__(self, method, fget=None, fset=None, fdel=None, doc=None):
        self.method = method
        self.cache_name = f'_{self.method.__name__}'

        doc = doc or method.__doc__
        super(lazyproperty, self).__init__(fget=fget, fset=fset, fdel=fdel, doc=doc)

        update_wrapper(self, method)

    def __get__(self, instance, owner):
        if instance is None:
            return self

        result = getattr(instance, self.cache_name, None)
        if result is None:
            result = (self.fget or self.method)(instance)
            setattr(instance, self.cache_name, result)
        return result


class lazymutable(lazyproperty):
    def __set__(self, instance, value):
        if instance is None:
            raise AttributeError

        if self.fset is None:
            setattr(instance, self.cache_name, value)
        else:
            self.fset(instance, value)


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
