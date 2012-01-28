from zope.interface import implements
from zope.publisher.browser import TestRequest as baseRequest

# from Products.Five import zcml
from Zope2.App import zcml
from Products.Five import fiveconfigure

from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import onsetup

from z3c.form.interfaces import IFormLayer


@onsetup
def setup_product():
    """
       Set up the package and its dependencies.
    """

    fiveconfigure.debug_mode = True
    import collective.geo.settings
    zcml.load_config('configure.zcml', collective.geo.settings)

    fiveconfigure.debug_mode = False


setup_product()
ptc.setupPloneSite(extension_profiles=['collective.geo.settings:default'])


class TestRequest(baseRequest):
    implements(IFormLayer)


class TestCase(ptc.PloneTestCase):
    pass


class FunctionalTestCase(ptc.FunctionalTestCase):
    pass
