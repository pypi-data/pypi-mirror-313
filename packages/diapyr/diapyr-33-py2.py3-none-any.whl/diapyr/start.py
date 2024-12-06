from .iface import Special
from .match import ExactMatch

class Started(Special): pass

def starter(startabletype):
    try:
        starter = startabletype.di_starter
    except AttributeError:
        pass
    else:
        match, = starter.__init__.di_deptypes
        if match.clazz == startabletype: # Otherwise it's inherited.
            return starter
    from .diapyr import types
    @types(ExactMatch(startabletype))
    def __init__(self, startable):
        startable.start()
        self.startable = startable
    def dispose(self):
        self.startable.stop() # FIXME: Untested.
    startabletype.di_starter = startedtype = type("Started[%s]" % Special.gettypelabel(startabletype), (Started,), {f.__name__: f for f in [__init__, dispose]})
    return startedtype
