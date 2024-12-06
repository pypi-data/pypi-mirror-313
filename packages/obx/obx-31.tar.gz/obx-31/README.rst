**NAME**


::

    OBX - a clean namespace.


**SYNOPSIS**

::

    >>> from obx import *
    >>> o = Object()
    >>> o.a = "b"
    >>> str(loads(dumps(o)))
    "{'a': 'b'}"


**DESCRIPTION**


::

    *OBX* contains all the python3 code to program objects in a functional
    way. It provides a base Object class that has only dunder methods, all
    methods are factored out into functions with the objects as the first
    argument. It is called Object Programming (OP), OOP without the
    oriented.

    *OBX* allows for easy json save//load to/from disk of objects. It
    provides an "clean namespace" Object class that only has dunder
    methods, so the namespace is not cluttered with method names. This
    makes storing and reading to/from json possible.


**INSTALL**

::

    $ pipx install obx
    $ pipx ensurepath


**SOURCE**

::

    source is at https://github.com/otpcr/obx


**AUTHOR**

::

    Bart Thate <bthate@dds.nl>


**COPYRIGHT**


::

    OBX is Public Domain.
