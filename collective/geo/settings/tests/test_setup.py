import unittest
from zope.component import getUtility
from zope.component import queryAdapter
from plone.registry.interfaces import IPersistentField
from plone.registry.interfaces import IRegistry

from collective.geo.settings.interfaces import IGeoSettings

from collective.geo.settings.tests.base import TestCase
from collective.geo.settings import schema


class TestSetup(TestCase):

    def test_decimal_persistentfield(self):
        field = schema.Coordinate(title=u"Test")
        self.failUnless(queryAdapter(field, IPersistentField))

    def test_viewlet_manager_props(self):
        registry = getUtility(IRegistry)
        geo_settings = registry.forInterface(IGeoSettings)
        self.assertTrue(hasattr(geo_settings, 'map_viewlet_managers'))

        default_managers = ["plone.abovecontentbody", "plone.belowcontentbody"]
        cgeo_vman = geo_settings.map_viewlet_managers
        for vman in default_managers:
            self.assertTrue(vman in cgeo_vman)


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestSetup))
    return suite
