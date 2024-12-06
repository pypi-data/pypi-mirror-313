class MissingAnnotationException(Exception): pass

class Special(object):

    @classmethod
    def gettypelabel(cls, type):
        try:
            subclass = issubclass(type, cls)
        except TypeError:
            subclass = False
        return type.__name__ if subclass else "%s:%s" % (type.__module__, type.__name__)

class UnsatisfiableRequestException(Exception): pass

class ImpasseException(Exception): pass

unset = object()
