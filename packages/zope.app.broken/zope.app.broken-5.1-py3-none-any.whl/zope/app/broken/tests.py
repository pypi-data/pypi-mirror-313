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
"""Broken-object tests

"""
import unittest
from doctest import DocTestSuite

from ZODB.broken import BrokenModified
from zope.configuration import xmlconfig
from zope.testing import cleanup

from zope.app.broken.broken import Broken


class TestBroken(unittest.TestCase):

    def tearDown(self):
        import ZODB.broken
        ZODB.broken.broken_cache.clear()

    def test_annotations(self):
        # Broken objects may have attribute annotations.
        # If so, we can access them.
        b = Broken()
        b.__setstate__({'__annotations__': {'foo.bar': 42}})
        self.assertEqual(42, b['foo.bar'])
        self.assertEqual(42, b.get('foo.bar'))

        # Missing keys are handled as expected
        self.assertRaises(KeyError, b.__getitem__, 'foo.baz')

        # Annotations can't be modified
        self.assertRaises(BrokenModified, b.__setitem__, 'foo.baz', 1)
        self.assertRaises(BrokenModified, b.__delitem__, 'foo.baz')

        # If there are no annotation data, then, obviously, there are
        # no annotations:
        b = Broken()
        self.assertIsNone(b.get('foo.bar'))
        self.assertRaises(KeyError, b.__getitem__, 'foo.bar')
        self.assertRaises(BrokenModified, b.__setitem__, 'foo.baz', 1)
        self.assertRaises(BrokenModified, b.__delitem__, 'foo.baz')

    def test__parent__(self):
        # parent comes from the state
        b = Broken()
        self.assertIsNone(b.__parent__)

        b.__setstate__({'__parent__': self})

        self.assertIs(self, b.__parent__)

    def test__name__(self):
        # name comes from the state
        b = Broken()
        self.assertIsNone(b.__name__)

        b.__setstate__({'__name__': self})

        self.assertIs(self, b.__name__)


class TestConfiguration(cleanup.CleanUp,
                        unittest.TestCase):

    def test_configure(self):
        xmlconfig.string(r"""
        <configure xmlns="http://namespaces.zope.org/browser"
                   i18n_domain="zope">
        <include package="zope.browsermenu" file="meta.zcml" />
        <menu
          id="zmi_views"
          title="Views"
          />

        <menu
          id="zmi_actions"
          title="Actions"
        />
        </configure>
        """)

        xmlconfig.string(r"""
        <configure xmlns="http://namespaces.zope.org/zope">
          <include package="zope.app.broken" />
        </configure>
        """)
        from zope.interface import implementer
        from zope.publisher.interfaces.browser import IDefaultBrowserLayer

        from zope import component

        @implementer(IDefaultBrowserLayer)
        class Layer:
            pass

        self.assertIsNotNone(component.getMultiAdapter(
            (Broken(), Layer()),
            name='index.html'))


def test_suite():
    return unittest.TestSuite((
        DocTestSuite('zope.app.broken.broken'),
        unittest.defaultTestLoader.loadTestsFromName(__name__),
    ))
