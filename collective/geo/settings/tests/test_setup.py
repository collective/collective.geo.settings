import unittest
from zope.component import queryAdapter
from plone.registry.interfaces import IPersistentField

from collective.geo.settings.tests.base import GeoSettingsTestCase
from collective.geo.settings import schema


class TestSetup(GeoSettingsTestCase):

    def test_decimal_persistentfield(self):
        field = schema.Coordinate(title=u"Test")
        self.failUnless(queryAdapter(field, IPersistentField))


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestSetup))
    return suite
