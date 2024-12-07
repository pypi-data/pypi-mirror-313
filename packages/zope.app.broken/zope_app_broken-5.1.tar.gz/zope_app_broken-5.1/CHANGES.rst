=========
 CHANGES
=========

5.1 (2024-12-06)
================

- Add support for Python 3.12, 3.13.

- Drop support for Python 3.7.


5.0 (2023-02-08)
================

- Add support for Python 3.10, 3.11.

- Drop support for Python 2.7, 3.5, 3.6.

- Remove ``zope.app.broken.interfaces.IBroken``. It had been moved to
  ``ZODB.interfaces`` long ago.


4.2 (2020-11-18)
================

- Deprecate ``zope.app.broken.interfaces.IBroken``. Please import it directly
  from ``ZODB.interfaces``.

- Add support for Python 3.9.

4.1 (2020-03-31)
================

- Drop dependency on ``zope.broken``, because the correct imports have
  moved into ZODB.

- Add support for Python 3.7 and 3.8.


4.0.0 (2017-05-16)
==================

- Add support for Python 3.4, 3.5, 3.6 and PyPy.

- Change dependency on ``ZODB3`` to ``ZODB``.

- The ``browser.zcml`` will only be loaded if ``zope.browserpage`` is
  installed.

- Accessing the ``__parent__`` and ``__name__`` attributes of broken
  objects will no longer raise ``AttributeError`` if the state is an
  unexpected type, instead returning ``None``.


3.6.0 (2010-09-25)
==================

- Depend on new ``zope.processlifetime`` interfaces and implementations
  instead of using BBB imports from ``zope.app.appsetup``.

- Added test extra to declare test dependency on ``zope.testing``.

- Using Python's ``doctest`` module instead of depreacted
  ``zope.testing.doctest``.


3.5.0 (2009-02-05)
==================

- Depend on new ``zope.broken`` package for the ``IBroken`` interface.

3.4.0 (2007-10-11)
==================

- Initial release independent of the main Zope tree.
