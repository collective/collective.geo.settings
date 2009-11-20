from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile
from zope.publisher.browser import BrowserView
from zope.component import getUtility

from collective.geo.settings.interfaces import IGeoSettings

class GeoSettingsView(object):
    """ Geo Settings macros """
    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.geosettings = getUtility(IGeoSettings)

    @property
    def zoom(self):
        return  self.geosettings.zoom

    @property
    def map_center(self):
        return self.geosettings.longitude, self.geosettings.latitude

    @property
    def googlemaps(self):
        return  self.geosettings.googlemaps

    @property
    def googleapi(self):
        return  self.geosettings.googleapi

    @property
    def google_maps_js(self):
        if self.googlemaps:
            return 'http://maps.google.com/maps?file=api&v=2&key=%s' % self.googleapi
        else:
            return None

    @property
    def yahoomaps(self):
        return self.geosettings.yahoomaps

    @property
    def yahooapi(self):
        return  self.geosettings.yahooapi

    @property
    def yahoo_maps_js(self):
        if self.yahoomaps:
            return 'http://api.maps.yahoo.com/ajaxymap?v=3.8&appid=%s' % self.yahooapi
        else:
            return None

    @property
    def bingmaps(self):
        return self.geosettings.bingmaps

    @property
    def bing_maps_js(self):
        if self.bingmaps:
            return 'http://dev.virtualearth.net/mapcontrol/mapcontrol.ashx?v=6'
        else:
            return None

    @property
    def geo_setting_js(self):
        lon, lat  = self.map_center
        state = { 'lon': lon,
                  'lat': lat,
                  'zoom': self.zoom }
        # set default configuration
        ret = ["cgmap.state = {'default': {lon: %(lon)7f, lat: %(lat)7f, zoom: %(zoom)d }};" % state]
        # go through all maps in request and extract their state
        # to update map_state
        for mapid in self.request.get('cgmap_state_mapids', '').split():
            map_state = self.request.get('cgmap_state.%s' % mapid)
            state = {'mapid': mapid}
            for param in ('lon', 'lat', 'zoom', 'activebaselayer', 'activelayers'):
                val = map_state.get(param, None)
                state[param] = (val is not None) and ("'%s'" % val) or 'undefined'
            ret.append("cgmap.state['%(mapid)s'] = {lon: %(lon)s, lat: %(lat)s, zoom: %(zoom)s, activebaselayer: %(activebaselayer)s, activelayers: %(activelayers)s };" % state)
        return '\n'.join(ret)

class GeoSettingsMacros(BrowserView):
    template = ViewPageTemplateFile('macros.pt')

    def __getitem__(self, key):
        return self.template.macros[key]
