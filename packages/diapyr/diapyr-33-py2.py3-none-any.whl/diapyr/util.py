from inspect import isfunction
import sys

ispy2 = sys.version_info.major < 3

class Proxy(object):

    def __getattr__(self, name):
        try:
            return getattr(self._enclosinginstance, name)
        except AttributeError:
            superclass = super(Proxy, self)
            try:
                supergetattr = superclass.__getattr__
            except AttributeError:
                raise AttributeError("'%s' object has no attribute '%s'" % (type(self).__name__, name))
            return supergetattr(name)

def innerclass(cls):
    'An instance of the decorated class may access its enclosing instance via `self`.'
    class InnerMeta(type):
        def __get__(self, enclosinginstance, owner):
            clsname = (cls if self is Inner else self).__name__
            return type(clsname, (Proxy, self), dict(_enclosinginstance = enclosinginstance))
    Inner = InnerMeta('Inner', (cls,), {})
    return Inner

def singleton(t):
    'The decorated class is replaced with a no-arg instance.'
    return t()

@singleton
class outerzip:

    class Session:

        def __init__(self, iterables):
            self.iterators = [iter(i) for i in iterables]

        def row(self):
            self.validrow = len(self.iterators)
            for i in self.iterators:
                try:
                    yield next(i)
                except StopIteration:
                    self.validrow -= 1
                    yield

    def __call__(self, *iterables):
        session = self.Session(iterables)
        while True:
            values = tuple(session.row())
            if not session.validrow:
                break
            yield values

def enum(*lists):
    def d(cls):
        cls.enum = v = []
        for args in lists:
            obj = cls(*args)
            setattr(cls, args[0], obj)
            v.append(obj)
        return cls
    return d

def _rootcontext(e):
    while True:
        c = getattr(e, '__context__', None)
        if c is None:
            return e
        e = c

def invokeall(callables):
    '''Invoke every callable, even if one or more of them fail. This is mostly useful for synchronising with futures.
    If all succeeded return their return values as a list, otherwise raise all exceptions thrown as a chain.'''
    values = []
    failure = None
    for c in callables:
        try:
            obj = c()
        except Exception as e:
            _rootcontext(e).__context__ = failure
            failure = e
        else:
            values.append(obj)
    if failure is None:
        return values
    raise failure

def bfs(keys):
    '''Breadth-first search starting with the given iterable of keys, intended to be used as a decorator.
    If a function is decorated it should take an info object and key, and yield subsequent keys.
    If a class is decorated, a new instance of it is used as info object:
    The class should have a `newdepth` method that will be called before each depth, and a `process` method that takes a key and yields subsequent keys as in the function case.
    The info object is kept updated with the list of `currentkeys`, current `depth` and the set of `donekeys`.
    Note that the first `currentkeys` (`depth` 0) is exactly the passed in `keys` iterable, subsequent `currentkeys` will be non-empty lists.
    The process function is only invoked for keys that have not yet been processed, i.e. unique keys.
    When finished the decorated function/class is replaced with the last state of the info object.'''
    def transform(function_or_class):
        if isfunction(function_or_class):
            class Info:
                def newdepth(self):
                    pass
                def process(self, key):
                    return function_or_class(self, key)
            info = Info()
        else:
            info = function_or_class()
        nextkeys = keys
        info.depth = -1
        info.donekeys = set()
        while True:
            iterator = iter(nextkeys)
            try:
                key = next(iterator)
            except StopIteration:
                break
            info.currentkeys = nextkeys
            info.depth += 1
            info.newdepth()
            nextkeys = []
            while True:
                if key not in info.donekeys:
                    j = info.process(key)
                    if j is not None:
                        nextkeys.extend(j)
                    info.donekeys.add(key)
                try:
                    key = next(iterator)
                except StopIteration:
                    break
        return info
    return transform
