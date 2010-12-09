from zope.interface import implements
from zope.schema import vocabulary

from zope.app.schema.vocabulary import IVocabularyFactory

from Products.CMFCore.utils import getToolByName

from collective.geo.settings import DISPLAY_PROPERTIES

# config for possible viewlet managers
PROPERTY_SHEET = 'collective_geo_settings_properties'
PROPERTY_DEFAULT_MAP_MANAGER = 'default_map_manager'
PROPERTY_MAP_MANAGERS = 'map_managers'

class baseVocabulary(object):
    implements(IVocabularyFactory)
    terms = []

    def __call__(self, context):
        terms = []
        for term in self.terms:
            terms.append(vocabulary.SimpleVocabulary.createTerm(term[0],
                                                                term[0],
                                                                term[1]))

        return vocabulary.SimpleVocabulary(terms)


class displaypropertiesVocab(baseVocabulary):
    terms = DISPLAY_PROPERTIES

class managerpropertiesVocab(baseVocabulary):

    def __call__(self, context):
        terms = []
        portal_props = getToolByName(context, 'portal_properties')
        properties = getattr(portal_props, PROPERTY_SHEET, None)
        if properties:
            self.terms = getattr(properties, PROPERTY_MAP_MANAGERS, [])
            for term in self.terms:
                terms.append(vocabulary.SimpleVocabulary.createTerm(term,
                                                                    term,
                                                                    term))
        return vocabulary.SimpleVocabulary(terms)

