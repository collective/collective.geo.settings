import unittest
from zope.testing import doctest
from collective.geo.settings.tests import base

import collective.geo.settings.geoconfig

from zope.component import provideUtility
from collective.geo.settings import geoconfig
from collective.geo.settings import interfaces

def setUp(test):
    # registrazione della mia utility .. componentregistry.xml
    provideUtility(
              geoconfig.GeoSettings,
              provides = interfaces.IGeoSettings
              )


def test_suite():
    return unittest.TestSuite((

        doctest.DocTestSuite(collective.geo.settings.geoconfig,
                     setUp=setUp,
                     optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS,),
        ))
