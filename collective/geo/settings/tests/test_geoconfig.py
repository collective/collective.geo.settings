import unittest
from zope.testing import doctest, doctestunit
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


def tearDown(test):
    """This is the companion to setUp - it can be used to clean up the 
    test environment after each test.
    """
    
def test_suite():
    return unittest.TestSuite((

        doctest.DocTestSuite(collective.geo.settings.geoconfig,
                     setUp=setUp, 
                     tearDown=tearDown,
                     optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS,),
        ))
