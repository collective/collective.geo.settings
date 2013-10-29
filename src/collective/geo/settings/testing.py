# -*- coding: utf-8 -*-
from zope.interface import implements
from zope.publisher.browser import TestRequest as baseRequest
from z3c.form.interfaces import IFormLayer

from plone.app.testing import PloneWithPackageLayer
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting

import collective.geo.settings


CGEO_SETTINGS = PloneWithPackageLayer(
    zcml_package=collective.geo.settings,
    zcml_filename='configure.zcml',
    gs_profile_id='collective.geo.settings:default',
    name="CGEO_SETTINGS")

CGEO_SETTINGS_INTEGRATION = IntegrationTesting(
    bases=(CGEO_SETTINGS, ),
    name="CGEO_SETTINGS_INTEGRATION")

CGEO_SETTINGS_FUNCTIONAL = FunctionalTesting(
    bases=(CGEO_SETTINGS, ),
    name="CGEO_SETTINGS_FUNCTIONAL")


class TestRequest(baseRequest):
    implements(IFormLayer)
