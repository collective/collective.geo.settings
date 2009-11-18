from Products.Five import zcml
from Products.Five import fiveconfigure

from Testing import ZopeTestCase as ztc

from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import onsetup

from Products.CMFPlone.utils import _createObjectByType

@onsetup
def setup_product():
    """
       Set up the package and its dependencies.
    """

    fiveconfigure.debug_mode = True
    import collective.geo.kml, collective.geo.settings
    zcml.load_config('configure.zcml', collective.geo.kml)
    zcml.load_config('configure.zcml', collective.geo.settings)

    fiveconfigure.debug_mode = False

    #ztc.installPackage('collective.geo.settings')

setup_product()
ptc.setupPloneSite(products=['collective.geo.kml', 'collective.geo.settings'])

class GeoSettingsTestCase(ptc.PloneTestCase):
    pass

class GeoSettingsFunctionalTestCase(ptc.FunctionalTestCase):

    def afterSetUp(self):
        self.setRoles(('Manager',))

        lpf = self.portal.portal_types['Topic']
        lpf_allow = lpf.global_allow
        lpf.global_allow = True

        _createObjectByType("Folder", self.portal, 'test_folder')
        _createObjectByType("Topic", self.portal, 'test_topic')

