from zope.app.pagetemplate import viewpagetemplatefile
from zope.component import getUtility
from collective.geo.settings.interfaces import IGeoSettings
from collective.geo.settings.geoconfig import GeoContainerSettings
class GeoSettingsMacros(object):
    """ Geo Settings macros """

    def __init__(self, context, request):
        self.geosettings = getUtility(IGeoSettings)
        self.context = context
        self.containersettings = GeoContainerSettings(self.context)
        self.containersettings.initialiseSettings(self.context)

    @property
    def use_custom_settings(self):
        return self.containersettings.get('use_custom_settings')

    @property
    def zoom(self):
        if self.use_custom_settings:
            return  self.containersettings.get('zoom')
        else:
            return  self.geosettings.zoom

    @property
    def googlemaps(self):
        if self.use_custom_settings:
            return  self.containersettings.get('googlemaps')
        else:
            return  self.geosettings.googlemaps

    @property
    def googleapi(self):
        return  self.geosettings.googleapi

    @property
    def map_center(self):
        if self.use_custom_settings:
            return  self.containersettings.get('longitude'), self.containersettings.get('latitude')
        else:
            return  self.geosettings.longitude, self.geosettings.latitude

    @property
    def geo_setting_js(self):
        googlemaps = self.googlemaps and 'true' or 'false'
        map_center = self.map_center
        return "var lon = %7f;\nvar lat = %7f;\nvar googlemaps = %s;\nvar zoom = %f;\n" % (map_center[0], self.map_center[1], googlemaps, self.zoom)

    @property
    def google_maps_js(self):
        if self.googlemaps:
            return 'http://maps.google.com/maps?file=api&v=2&key=%s' % self.googleapi
        else:
            return None
