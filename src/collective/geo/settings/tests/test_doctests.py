import unittest2 as unittest
import doctest

from plone.testing import layered
from ..testing import CGEO_SETTINGS_INTEGRATION

import collective.geo.settings.schema


def test_suite():
    suite = unittest.TestSuite()
    suite.addTests([
        layered(doctest.DocFileSuite(
            'README.txt',
            package='collective.geo.settings',
            optionflags=doctest.REPORT_ONLY_FIRST_FAILURE | \
                doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
            ),
            layer=CGEO_SETTINGS_INTEGRATION
        ),

        layered(
            doctest.DocTestSuite(
                collective.geo.settings.schema,
                optionflags=doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
            ),
            layer=CGEO_SETTINGS_INTEGRATION
        ),

    ])
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
