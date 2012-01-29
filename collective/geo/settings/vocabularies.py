from zope.interface import implements
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.interfaces import IVocabularyFactory

from zope.component import getUtility

from plone.registry.interfaces import IRegistry

from collective.geo.settings import DISPLAY_PROPERTIES
from collective.geo.settings.interfaces import IGeoSettings
from collective.geo.settings import GeoSettingsMessageFactory as _


class baseVocabulary(object):
    implements(IVocabularyFactory)
    terms = []

    def __call__(self, context):
        terms = []
        for term in self.terms:
            terms.append(SimpleVocabulary.createTerm(term[0],
                                                    term[0],
                                                    term[1]))

        return SimpleVocabulary(terms)


class displaypropertiesVocab(baseVocabulary):
    terms = DISPLAY_PROPERTIES


class mapviewletmanagersVocab(baseVocabulary):

    @property
    def terms(self):
        registry = getUtility(IRegistry)
        geo_settings = registry.forInterface(IGeoSettings)
        terms = [('fake-manager', _(u'Do not display map'))]
        for i in geo_settings.map_viewlet_managers:
            elem = i.split('|')
            terms.append((elem[0],
                    len(elem) > 1 and elem[1] or elem[0]))
        return terms
