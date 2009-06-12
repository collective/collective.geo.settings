from zope.app.pagetemplate import viewpagetemplatefile
from zope.component import getUtility
from collective.geo.settings.interfaces import IGeoSettings
class GeoSettingsMacros(object):
    """ Geo Settings macros """
    def __init__(self, context, request):
        self.geosettings = getUtility(IGeoSettings)

    @property
    def zoom(self):
        return  self.geosettings.zoom

    @property
    def googlemaps(self):
        return  self.geosettings.googlemaps

    @property
    def googleapi(self):
        return  self.geosettings.googleapi

    @property
    def map_center(self):
        return  self.geosettings.latitude, self.geosettings.longitude

    @property
    def geo_setting_js(self):
        googlemaps = self.googlemaps and 'true' or 'false'
        map_center = self.map_center
        return "var lat = %7f;\nvar lon = %7f;\nvar googlemaps = %s;\nvar zoom = %d;\n" % (map_center[0], self.map_center[1], googlemaps, self.zoom)

    @property
    def google_maps_js(self):
        if self.googlemaps:
            return 'http://maps.google.com/maps?file=api&amp;v=2&amp;key=%s' % self.googleapi
        else:
            return None
