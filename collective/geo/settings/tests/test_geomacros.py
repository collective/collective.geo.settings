import unittest
from collective.geo.settings.tests import base
from collective.geo.settings.interfaces import IGeoSettings


class TestSetup(base.GeoSettingsTestCase):

    def afterSetUp(self):
        self.settings = self.portal.restrictedTraverse('@@geosettings-view')

    def test_property_zoom(self):
        self.assertEquals(self.settings.zoom, 10.0)

    def test_property_map_center(self):
        self.assertEquals(self.settings.map_center, (7.680470, 45.682143))

    def test_property_googlemaps(self):
        self.assertEquals(self.settings.googlemaps, True)

    def test_property_googleapi(self):
        self.assertEquals(self.settings.googleapi,
                          u'ABQIAAAAaKes6QWqobpCx2AOamo-shTwM0brOpm-All5BF6PoaKBxRWWERSUWbHs4SIAMkeC1KV98E2EdJKuJw')

    def test_property_jsgooglemaps(self):
        # IGeoSettings googlemaps == True
        self.assertEquals(self.settings.google_maps_js,
                          'http://maps.google.com/maps?file=api&v=2&key=ABQIAAAAaKes6QWqobpCx2AOamo-shTwM0brOpm-All5BF6PoaKBxRWWERSUWbHs4SIAMkeC1KV98E2EdJKuJw')

        # when IGeoSettings.googlemaps equals False self.settings.googleapi must be ''
        IGeoSettings(self.portal).googlemaps  = False
        self.assertEquals(self.settings.google_maps_js,
                          None)

    def test_property_yahoomaps(self):
        self.assertEquals(self.settings.yahoomaps, False)

    def test_property_yahooapi(self):
        self.assertEquals(self.settings.yahooapi,
                          u'YOUR_API_KEY')

    def test_property_jsyahoomaps(self):
        # IGeoSettings yahoomaps == True
        IGeoSettings(self.portal).yahoomaps  = True
        self.assertEquals(self.settings.yahoo_maps_js,
                          'http://api.maps.yahoo.com/ajaxymap?v=3.8&appid=YOUR_API_KEY')

        # when IGeoSettings.yahoomaps equals False self.settings.yahooapi must be ''
        IGeoSettings(self.portal).yahoomaps  = False
        self.assertEquals(self.settings.yahoo_maps_js,
                          None)

    def test_property_bingmaps(self):
        self.assertEquals(self.settings.bingmaps, False)

    def test_property_jsbingmaps(self):
        # IGeoSettings bingmaps == True
        IGeoSettings(self.portal).bingmaps  = True
        self.assertEquals(self.settings.bing_maps_js,
                          'http://dev.virtualearth.net/mapcontrol/mapcontrol.ashx?v=6')

        # when IGeoSettings.yahoomaps equals False self.settings.yahooapi must be ''
        IGeoSettings(self.portal).bingmaps  = False
        self.assertEquals(self.settings.bing_maps_js,
                          None)

    def test_property_geosettingjs(self):
        IGeoSettings(self.portal).googlemaps  = True
        self.assertEquals(self.settings.geo_setting_js,
                          "cgmap.state = {'default': {lon: 7.680470, lat: 45.682143, zoom: 10 }};")



def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestSetup))
    return suite
