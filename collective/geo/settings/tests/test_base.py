import unittest
import doctest

from zope.testing import doctestunit
from Testing import ZopeTestCase as ztc

from collective.geo.settings.tests import base

def test_suite():
    return unittest.TestSuite([

        ztc.ZopeDocFileSuite(
            'README.txt', package='collective.geo.settings',
            test_class=base.GeoSettingsFunctionalTestCase,
            optionflags=doctest.REPORT_ONLY_FIRST_FAILURE | doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
            ),


        ])