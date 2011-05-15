from zope.interface import implements
from zope.schema import vocabulary
from zope.schema.interfaces import IVocabularyFactory

from zope.component import getUtility

from plone.registry.interfaces import IRegistry

from collective.geo.settings import DISPLAY_PROPERTIES
from collective.geo.settings.interfaces import IGeoSettings


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


class mapviewletmanagersVocab(baseVocabulary):

    @property
    def terms(self):
        registry = getUtility(IRegistry)
        geo_settings = registry.forInterface(IGeoSettings)
        terms = [(None, 'Do not display map')]
        for i in geo_settings.map_viewlet_managers:
            terms.append((i, i))
        return terms
