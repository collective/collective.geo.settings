from zope.interface import implements
from zope.schema import vocabulary

from zope.app.schema.vocabulary import IVocabularyFactory

from collective.geo.settings import DISPLAY_PROPERTIES

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
