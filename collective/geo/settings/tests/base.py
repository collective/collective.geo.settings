from Products.Five import zcml
from Products.Five import fiveconfigure

from Testing import ZopeTestCase as ztc

from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import onsetup


@onsetup
def setup_product():
    """
       Set up the package and its dependencies.
    """

    fiveconfigure.debug_mode = True
    import collective.geo.settings
    zcml.load_config('configure.zcml', collective.geo.settings)

    fiveconfigure.debug_mode = False

    #ztc.installPackage('collective.geo.settings')

setup_product()
ptc.setupPloneSite(products=['collective.geo.settings'])

class GeoSettingsTestCase(ptc.PloneTestCase):
    pass

class GeoSettingsFunctionalTestCase(ptc.FunctionalTestCase):
    pass
