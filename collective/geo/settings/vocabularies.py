import pkg_resources
from Acquisition import aq_get
from zope.interface import implements
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.interfaces import IVocabularyFactory
from zope.i18n import translate

from zope.component import getUtility
from zope.site.hooks import getSite
from Products.CMFCore.utils import getToolByName

from plone.registry.interfaces import IRegistry
from plone.app.vocabularies.types import BAD_TYPES

from collective.geo.settings import DISPLAY_PROPERTIES
from collective.geo.settings.interfaces import IGeoSettings
from collective.geo.settings import GeoSettingsMessageFactory as _

try:
    pkg_resources.get_distribution('plone.dexterity')
except pkg_resources.DistributionNotFound:
    HAS_DEXTERITY = False
else:
    HAS_DEXTERITY = True
    from plone.dexterity.interfaces import IDexterityFTI


class baseVocabulary(object):
    implements(IVocabularyFactory)
    terms = []

    def __call__(self, context):
        terms = []
        for term in self.terms:
            terms.append(SimpleVocabulary.createTerm(
                term[0],
                term[0],
                term[1])
            )

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
            terms.append((
                elem[0],
                len(elem) > 1 and elem[1] or elem[0])
            )
        return terms


class ATTypesVocabulary(object):
    implements(IVocabularyFactory)

    def __call__(self, context):
        site = getSite()
        ttool = getToolByName(site, 'portal_types', None)
        if ttool is None:
            return SimpleVocabulary([])
        items = []
        request = aq_get(ttool, 'REQUEST', None)

        for k, v in ttool.items():
            if HAS_DEXTERITY:
                if IDexterityFTI.providedBy(v):
                    continue
            if k not in BAD_TYPES:
                items.append(
                    (k, translate(v.Title(), context=request))
                )

        items.sort(key=lambda x: x[1])
        items = [SimpleTerm(i[0], i[0], i[1]) for i in items]
        return SimpleVocabulary(items)
