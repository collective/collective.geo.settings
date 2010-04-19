import unittest
from zope.testing import doctest
# from collective.geo.settings.tests import base

import collective.geo.settings.schema


def test_suite():
    return unittest.TestSuite((

        doctest.DocTestSuite(collective.geo.settings.schema,
                     optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS)))
