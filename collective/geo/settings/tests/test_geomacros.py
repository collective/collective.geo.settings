import unittest
from collective.geo.settings.tests import base
from collective.geo.settings.interfaces import IGeoSettings


class TestSetup(base.GeoSettingsTestCase):

    def afterSetUp(self):
        self.settings = self.portal.restrictedTraverse('@@geosettings-macros')

    def test_property_zoom(self):
        self.assertEquals(self.settings.zoom, 10)

    def test_property_googleapi(self):
        self.assertEquals(self.settings.googleapi,
                          u'ABQIAAAAaKes6QWqobpCx2AOamo-shTwM0brOpm-All5BF6PoaKBxRWWERSUWbHs4SIAMkeC1KV98E2EdJKuJw')

    def test_property_googlemaps(self):
        self.assertEquals(self.settings.googlemaps, True)

    def test_property_jsgooglemaps(self):
        # IGeoSettings googlemaps == True
        self.assertEquals(self.settings.google_maps_js,
                          'http://maps.google.com/maps?file=api&amp;v=2&amp;key=ABQIAAAAaKes6QWqobpCx2AOamo-shTwM0brOpm-All5BF6PoaKBxRWWERSUWbHs4SIAMkeC1KV98E2EdJKuJw')

        # when IGeoSettings.googlemaps equals False self.settings.googleapi must be ''
        IGeoSettings(self.portal).googlemaps  = False
        self.assertEquals(self.settings.google_maps_js,
                          None)

    def test_property_geosettingjs(self):
        IGeoSettings(self.portal).googlemaps  = True
        self.assertEquals(self.settings.geo_setting_js,
                          'var lat = 45.682143;\nvar lon = 7.680470;\nvar googlemaps = true;\nvar zoom = 10;\n')



def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestSetup))
    return suite
