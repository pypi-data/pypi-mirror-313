.. image:: https://github.com/zopefoundation/zope.app.broken/workflows/tests/badge.svg
        :target: https://github.com/zopefoundation/zope.app.broken/actions?query=workflow%3Atests

When an object cannot be correctly loaded from the ZODB, this package allows
this object still to be instantiated, but as a "Broken" object. This allows
for gracefully updating the database without interruption.
