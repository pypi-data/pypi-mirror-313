##############################################################################
#
# Copyright (c) 2004 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""Broken-object support

"""
import ZODB.broken
import zope.interface
import zope.location.interfaces
import zope.security.checker
from ZODB.interfaces import IBroken
from zope.annotation.interfaces import IAnnotations


@zope.interface.implementer(
    IBroken,
    zope.location.interfaces.ILocation,
    IAnnotations,
)
class Broken(ZODB.broken.Broken):

    def __get_state(self, key, default=None):
        get = getattr(self.__Broken_state__, 'get', None)
        if get is None:
            def get(key, default):
                return default
        return get(key, default)

    @property
    def __parent__(self):
        return self.__get_state('__parent__')

    @property
    def __name__(self):
        return self.__get_state('__name__')

    def __getAnnotations(self):
        return self.__get_state('__annotations__', {})

    def __getitem__(self, key):
        return self.__getAnnotations()[key]

    def __setitem__(self, key, value):
        raise ZODB.broken.BrokenModified("Can't modify broken objects")

    def __delitem__(self, key):
        raise ZODB.broken.BrokenModified("Can't modify broken objects")

    def get(self, key, default=None):
        annotations = self.__getAnnotations()
        return annotations.get(key, default)


def installBroken(event):
    """Install a class factory that handled broken objects

    This method installs a custom class factory when it gets a
    database-opened event::

      >>> import ZODB.tests.util
      >>> from zope.processlifetime import DatabaseOpened
      >>> db = ZODB.tests.util.DB()
      >>> installBroken(DatabaseOpened(db))

    If someone tries to load an object for which there is no class,
    then they will get a `Broken` object. We can simulate that by
    calling the database's class factory directly with a connection
    (None will do for our purposes, since the class factory function
    we register ignores the connection argument), a non-existent
    module and class name::

      >>> cls = db.classFactory(None, 'ZODB.not.there', 'atall')

    The class that comes back is a subclass of `Broken`::

      >>> issubclass(cls, Broken)
      True

    It implements ILocation and IAnnotations::

      >>> zope.location.interfaces.ILocation.implementedBy(cls)
      True
      >>> IAnnotations.implementedBy(cls)
      True

    and it has a security checker that is the same as the checker that
    `Broken` has::

      >>> (cls.__Security_checker__ is
      ...     zope.security.checker.getCheckerForInstancesOf(Broken))
      True

    Cleanup:

      >>> ZODB.broken.broken_cache.clear()
    """

    Broken_ = Broken  # make it local for speed
    find_global = ZODB.broken.find_global

    def type_(name, bases, dict):
        cls = type(name, bases, dict)
        checker = zope.security.checker.getCheckerForInstancesOf(Broken_)
        cls.__Security_checker__ = checker
        return cls

    def classFactory(connection, modulename, globalname):
        return find_global(modulename, globalname, Broken_, type_)

    event.database.classFactory = classFactory
