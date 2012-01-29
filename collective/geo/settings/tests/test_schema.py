import unittest
import doctest
import collective.geo.settings.schema


def test_suite():
    return unittest.TestSuite((

        doctest.DocTestSuite(collective.geo.settings.schema,
                     optionflags=doctest.NORMALIZE_WHITESPACE |\
                                                doctest.ELLIPSIS)))
