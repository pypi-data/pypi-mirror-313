from .iface import UnsatisfiableRequestException, unset

class DefaultArg:

    sources = ()

    def __init__(self, default):
        self.default = default

    def resolve(self):
        return self.default

class SourceArg:

    @property
    def sources(self):
        yield self.source

    def __init__(self, source, trigger):
        self.source = source
        self.trigger = trigger

    def resolve(self):
        return self.source.instance

class ListArg:

    def __init__(self, sources, trigger):
        self.sources = sources
        self.trigger = trigger

    def resolve(self):
        return [s.instance for s in self.sources]

class BaseGetAll:

    def __init__(self, clazz):
        self.clazz = clazz

    def getsources(self, di):
        return [source for source in di.typetosources.get(self.clazz, []) if self.acceptsource(source)]

class GetAll(BaseGetAll):

    def acceptsource(self, source):
        return True

class AllInstancesOf(GetAll):

    def di_get(self, di, default):
        return ListArg(self.getsources(di), self.clazz)

class One:

    def di_get(self, di, default):
        sources = self.getsources(di)
        if not sources:
            if di.parent is not None:
                return self.di_get(di.parent, default) # XXX: Is parent thread-safe?
            if default is not unset:
                return DefaultArg(default)
        if 1 != len(sources):
            raise UnsatisfiableRequestException("Expected 1 object of type %s but got: %s" % (self.clazz, len(sources)))
        return SourceArg(sources[0], self.clazz)

class OneInstanceOf(GetAll, One): pass

class ExactMatch(BaseGetAll, One):

    def acceptsource(self, source):
        return self.clazz == source.type

def wrap(obj):
    if list == type(obj):
        componenttype, = obj
        return AllInstancesOf(componenttype)
    if hasattr(obj, 'di_get'):
        return obj
    return OneInstanceOf(obj)
