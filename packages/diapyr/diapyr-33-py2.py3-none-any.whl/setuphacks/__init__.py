from . import fakesetup
from traceback import format_exception_only
import os, subprocess, sys

class SetupException(Exception): pass

def getsetupkwargs(setuppath, fields):
    'Extract the kwargs passed to `setup` at the given path (typically some setup.py) that have names in the given `fields`.'
    cwd, = (dict(cwd = d) if d else {} for d in [os.path.dirname(setuppath)])
    setupkwargs = eval(subprocess.check_output([sys.executable, fakesetup.__file__, os.path.basename(setuppath)] + fields, **cwd))
    if isinstance(setupkwargs, BaseException):
        # Can't simply propagate SystemExit for example:
        raise SetupException(format_exception_only(setupkwargs.__class__, setupkwargs)[-1].rstrip())
    return setupkwargs
