# diapyr
Constructor injection for Python

## Usage examples

### Dependency injection
```
>>> from diapyr import DI, types
>>>
>>> class Config: pass
>>>
>>> class Database:
...
...     @types(Config)
...     def __init__(self, config):
...         self.conninfo = config.conninfo
...
>>> class Server:
...
...     @types(Config, Database)
...     def __init__(self, config, database):
...         self.port = config.port
...         self.database = database
...
...     def serve_forever(self):
...         print(self.port)
...
>>> config = Config()
>>> config.conninfo = 'dbname=test user=postgres'
>>> config.port = 8000
>>> with DI() as di:
...     di.add(config)
...     di.add(Database)
...     di.add(Server)
...     di(Server).serve_forever()
8000

```

### Java-style inner class
```
>>> from diapyr.util import innerclass
>>>
>>> class X:
...
...     @innerclass
...     class Y(object):
...
...         def bar(self):
...             return self.foo # Y can access all fields of the enclosing instance of X.
...
...     def __init__(self, foo):
...         self.foo = foo
...
>>> x = X(100)
>>> y = x.Y()
>>> y.bar()
100

```

## Overview
* Automatic wiring between application objects
* Declare what collaborator types you want in your constructor using an `@types` decorator, they correspond with params
    * You can decorate a (factory) function in the same way, in which case specify a return type using the `this` kwarg, or if left out the return type is the function itself
    * Surround a type in square brackets if you want a list of all matching objects, normally diapyr provides a unique match
* Add such classes/factories to a DI instance
    * You can also add objects, for example an application config object
* Request a type from the DI instance and diapyr will attempt to make it for you, along with the rest of the object graph
* Instances are cached in the DI object
    * On exit from `with` clause, `dispose` is called on any created instances that have it

## Motivation
* Manual wiring is messy and tedious especially when an app gets big
* Constructor injection avoids spaghetti code
* It's trivial to depend on an object anywhere in the graph as long as you don't create a reference cycle e.g. most objects will depend on the same config instance
    * No need to resort to globals, which come with a big risk of leaking state between unit tests
* Unit testing is easy when an object only interacts with what was passed into its constructor

## Convention
* When depending on a config object the constructor should first extract what it needs and assign those values to fields
* Collaborators should also be assigned to fields, and ideally the constructor won't do anything else

## Advanced
* Parameter defaults are honoured, this can be used to depend on a module's log object in real life but pass in a mock in unit tests
* Decorating an instance method (without `this` kwarg) will make it behave as an additional constructor
    * Take advantage of name mangling (start with double underscore e.g. `__init`) to avoid having to call super
* Decorating an instance method with `this` kwarg will make it behave as a factory function
    * Adding a class to DI will implicity add all such methods it has as factories
* You can play fast and loose with types, diapyr doesn't care whether a factoried object satisfies the declared type

## API

<a id="diapyr"></a>

### diapyr

<a id="diapyr.DI"></a>

###### DI

Convenience import.

<a id="diapyr.types"></a>

###### types

Convenience import.

<a id="diapyr.diapyr"></a>

### diapyr.diapyr

<a id="diapyr.diapyr.types"></a>

###### types

```python
def types(*deptypes, **kwargs)
```

Declare that the decorated function or method expects args of the given types. Use square brackets to request all instances of a type as a list. Use `this` kwarg to declare the type of result returned by a factory.

<a id="diapyr.diapyr.DI"></a>

#### DI Objects

```python
class DI()
```

<a id="diapyr.diapyr.DI.add"></a>

###### add

```python
def add(obj)
```

Register the given class, factory or instance.

<a id="diapyr.diapyr.DI.all"></a>

###### all

```python
def all(type)
```

Return all objects of the given type, instantiating them and collaborators if necessary.

<a id="diapyr.diapyr.DI.__call__"></a>

###### \_\_call\_\_

```python
def __call__(clazz)
```

Return unique object of the given type, instantiating it and its collaborators if necessary.

<a id="diapyr.diapyr.DI.__exit__"></a>

###### \_\_exit\_\_

```python
def __exit__(*exc_info)
```

Discard all instances created by this container, calling `dispose` if they have it.

<a id="diapyr.start"></a>

### diapyr.start

<a id="diapyr.util"></a>

### diapyr.util

<a id="diapyr.util.innerclass"></a>

###### innerclass

```python
def innerclass(cls)
```

An instance of the decorated class may access its enclosing instance via `self`.

<a id="diapyr.util.singleton"></a>

###### singleton

```python
def singleton(t)
```

The decorated class is replaced with a no-arg instance.

<a id="diapyr.util.invokeall"></a>

###### invokeall

```python
def invokeall(callables)
```

Invoke every callable, even if one or more of them fail. This is mostly useful for synchronising with futures.
If all succeeded return their return values as a list, otherwise raise all exceptions thrown as a chain.

<a id="diapyr.util.bfs"></a>

###### bfs

```python
def bfs(keys)
```

Breadth-first search starting with the given iterable of keys, intended to be used as a decorator.
If a function is decorated it should take an info object and key, and yield subsequent keys.
If a class is decorated, a new instance of it is used as info object:
The class should have a `newdepth` method that will be called before each depth, and a `process` method that takes a key and yields subsequent keys as in the function case.
The info object is kept updated with the list of `currentkeys`, current `depth` and the set of `donekeys`.
Note that the first `currentkeys` (`depth` 0) is exactly the passed in `keys` iterable, subsequent `currentkeys` will be non-empty lists.
The process function is only invoked for keys that have not yet been processed, i.e. unique keys.
When finished the decorated function/class is replaced with the last state of the info object.

<a id="setuphacks"></a>

### setuphacks

<a id="setuphacks.getsetupkwargs"></a>

###### getsetupkwargs

```python
def getsetupkwargs(setuppath, fields)
```

Extract the kwargs passed to `setup` at the given path (typically some setup.py) that have names in the given `fields`.

