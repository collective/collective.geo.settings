import unittest
from zope.component import getUtility, queryUtility
from zope.component import queryAdapter
from zope.schema.interfaces import IVocabularyFactory

from plone.registry.interfaces import IPersistentField
from plone.registry.interfaces import IRegistry

from collective.geo.settings.interfaces import IGeoSettings
from collective.geo.settings.interfaces import IGeoFeatureStyle

from collective.geo.settings.tests.base import TestCase
from collective.geo.settings import schema


class TestSetup(TestCase):

    def test_decimal_persistentfield(self):
        field = schema.Coordinate(title=u"Test")
        self.failUnless(queryAdapter(field, IPersistentField))

    def test_viewlet_managers_props(self):
        registry = getUtility(IRegistry)
        settings = registry.forInterface(IGeoSettings)
        self.assertTrue(hasattr(settings, 'map_viewlet_managers'))

        default_managers = [u'plone.abovecontentbody|Above Content',
                            u'plone.belowcontentbody|Below Content']

        cgeo_vman = settings.map_viewlet_managers
        for vman in default_managers:
            self.assertTrue(vman in cgeo_vman)

    def test_viewlet_managers_vocabulary(self):
        vocabulary = queryUtility(IVocabularyFactory,
                        name="mapviewletmanagersVocab")(self.portal)
        self.failUnless(vocabulary)
        
        self.assertEquals(len(vocabulary._terms), 3)

    def test_map_viewlet_position(self):
        registry = getUtility(IRegistry)
        settings = registry.forInterface(IGeoFeatureStyle)
        self.assertTrue(hasattr(settings, 'map_viewlet_position'))


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestSetup))
    return suite
