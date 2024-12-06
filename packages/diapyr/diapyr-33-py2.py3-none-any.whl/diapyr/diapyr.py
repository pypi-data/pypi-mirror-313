from .iface import ImpasseException, MissingAnnotationException, unset
from .match import AllInstancesOf, wrap
from .source import Builder, Class, Factory, Instance, Proxy
from .start import starter
from .util import bfs, invokeall, singleton
from collections import defaultdict, OrderedDict
from inspect import isfunction
import logging

log = logging.getLogger(__name__)
typeitself = type

@singleton
class NullPlan:

    args = ()

    def make(self):
        pass

def types(*deptypes, **kwargs):
    'Declare that the decorated function or method expects args of the given types. Use square brackets to request all instances of a type as a list. Use `this` kwarg to declare the type of result returned by a factory.'
    def g(f):
        f.di_deptypes = tuple(wrap(t) for t in deptypes)
        if 'this' in kwargs:
            f.di_owntype = kwargs['this']
        return f
    return g

class DI:

    log = log # Tests may override.
    depthunit = '>'

    def __init__(self, parent = None):
        self.typetosources = defaultdict(list)
        self.allsources = [] # Old-style classes won't be registered against object.
        self.parent = parent

    def addsource(self, source):
        for type in source.types:
            self.typetosources[type].append(source)
        self.allsources.append(source)

    def removesource(self, source): # TODO: Untested.
        for type in source.types:
            self.typetosources[type].remove(source)
        self.allsources.remove(source)

    def addclass(self, clazz):
        try:
            clazz.__init__.di_deptypes
        except AttributeError:
            raise MissingAnnotationException("Missing types annotation: %s" % clazz)
        self.addsource(Class(clazz, self))
        self._addbuilders(clazz)
        if getattr(clazz, 'start', None) is not None:
            self.addclass(starter(clazz))

    def _addbuilders(self, cls):
        for name in dir(cls):
            m = getattr(cls, name)
            if hasattr(m, 'di_deptypes') and hasattr(m, 'di_owntype'):
                assert '__init__' != name # TODO LATER: Check upfront.
                self.addsource(Builder(cls, m, self))

    def addinstance(self, instance, type = None):
        clazz = instance.__class__ if type is None else type
        self.addsource(Instance(instance, clazz))
        if not isinstance(instance, typeitself):
            self._addbuilders(clazz)

    def addfactory(self, factory):
        self.addsource(Factory(factory, self))

    def _addmethods(self, obj):
        if hasattr(obj, 'di_owntype') or isfunction(obj):
            yield self.addfactory
        elif hasattr(obj, '__class__'):
            clazz = obj.__class__
            if clazz == type: # It's a non-fancy class.
                yield self.addclass
            elif isinstance(obj, type): # It's a fancy class.
                yield self.addinstance
                try:
                    obj.__init__.di_deptypes
                    yield self.addclass
                except AttributeError:
                    pass # Not admissible as class.
            else: # It's an instance.
                yield self.addinstance
        else: # It's an old-style class.
            yield self.addclass

    def add(self, obj):
        'Register the given class, factory or instance.'
        for m in self._addmethods(obj):
            m(obj)

    def all(self, type):
        'Return all objects of the given type, instantiating them and collaborators if necessary.'
        return self._session(AllInstancesOf(type))

    def __call__(self, clazz):
        'Return unique object of the given type, instantiating it and its collaborators if necessary.'
        return self._session(wrap(clazz))

    def _session(self, match):
        root = match.di_get(self, unset)
        plans = OrderedDict()
        @bfs([root])
        def proc(info, a):
            for s in a.sources:
                if s not in plans:
                    p = s.plan(self.depthunit * info.depth, a.trigger)
                    if p is None:
                        p = NullPlan
                    plans[s] = p
                    for b in p.args:
                        yield b
        while plans:
            sources = [s for s in plans if not any(r in plans for a in plans[s].args for r in a.sources)]
            if not sources:
                raise ImpasseException
            for s in sources:
                plans.pop(s).make()
        return root.resolve()

    def join(self, type, discardall = True):
        self.parent.addsource(Proxy(self, type, discardall))

    def __enter__(self):
        return self

    def __exit__(self, *exc_info):
        'Discard all instances created by this container, calling `dispose` if they have it.'
        self.discardall()

    def discardall(self):
        invokeall([s.discard for s in reversed(self.allsources)])
