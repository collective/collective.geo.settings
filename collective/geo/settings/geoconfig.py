from persistent import Persistent
from zope.interface import implements
from collective.geo.settings.interfaces import IGeoSettings
from zope.component import getUtility

class GeoSettings(Persistent):
    """
        GeoSettings have some propreties. We can get its propterties directly
        >>> config = GeoSettings()
        >>> config.zoom
        10.0

        or by the 'get' method
        >>> config.get('googlemaps')
        True

        we can set GeoSettins in this way
        >>> config.zoom = 9.5
        >>> config.zoom
        9.5

        or by the 'set' method
        >>> config.set('zoom', 10.0)
        >>> config.zoom
        10.0

    """
    implements(IGeoSettings)

    latitude = 45.682143
    longitude = 7.68047
    zoom = 10.0
    googlemaps = True
    googleapi = 'ABQIAAAAaKes6QWqobpCx2AOamo-shTwM0brOpm-All5BF6PoaKBxRWWERSUWbHs4SIAMkeC1KV98E2EdJKuJw'

    yahoomaps = False # turned off by default
    yahoomapapi = 'YOUR_API_KEY'

    bingmaps = False # turned off by default

    # TODO: turn this into a Folder (or some sort of btree/dict storage), and manage layers as content objects in this folder
    layers = {'osm': """new OpenLayers.Layer.TMS(
                           'OpenStreetMap',
                           'http://tile.openstreetmap.org/',
                           { type : 'png',
                             getURL: osm_getTileURL,
                             displayOutsideMaxExtent: true,
                             attribution: '<a href="http://www.openstreetmap.org/">OpenStreetMap</a>'})""",
              # 'oam': """new OpenLayers.Layer.TMS(
              #              'OpenAerialMap',
              #              'http://tile.openaerialmap.org/tiles/1.0.0/openaerialmap-900913/',
              #              { type: 'png',
              #                getURL: osm_getTileURL })""",
              'bmap': """new OpenLayers.Layer.VirtualEarth(
                              'Bing Streets',
                              { type: VEMapStyle.Shaded,
                                sphericalMercator: true })""",
              # .Road
              'baer': """new OpenLayers.Layer.VirtualEarth(
                             'Bing Aerial',
                             { type: VEMapStyle.Aerial,
                               sphericalMercator: true })""",
              'bhyb': """new OpenLayers.Layer.VirtualEarth(
                             'Bing Hybrid',
                             { type: VEMapStyle.Hybrid,
                               sphericalMercator: true })""",
              'gmap': """new OpenLayers.Layer.Google(
                            'Google',
                            {sphericalMercator: true})""",
              'gsat': """new OpenLayers.Layer.Google(
                            'Satellite (Google)' ,
                            {type: G_SATELLITE_MAP, sphericalMercator: true})""",
              'ghyb': """new OpenLayers.Layer.Google(
                            'Hybrid (Google)' ,
                            {type: G_HYBRID_MAP, sphericalMercator: true})""",
              'gter': """new OpenLayers.Layer.Google(
                            'Terrain (Google)' ,
                            {type: G_PHYSICAL_MAP, sphericalMercator: true})""",
              'ymap': """new OpenLayers.Layer.Yahoo(
                            'Yahoo Street',
                            {sphericalMercator: true})""",
              'ysat': """new OpenLayers.Layer.Yahoo(
                            'Yahoo Satellite',
                            {type: YAHOO_MAP_SAT, sphericalMercator: true})""",
              'yhyb': """new OpenLayers.Layer.Yahoo(
                            'Yahoo Hybrid',
                            {type: YAHOO_MAP_HYB, sphericalMercator: true})"""
              }

    def set(self, key,  val):
        return self.__setattr__(key, val)

    def get(self, key,  default=False):
        try:
            return self.__getattribute__(key)
        except:
            return default

class GeoConfig(object):
    """
        Non ho ancora capito a cosa serva sto coso
        We get the IGeoSettings utility
        >>> config = GeoConfig()
        >>> config.getSettings()
        <class 'collective.geo.settings.geoconfig.GeoSettings'>

        and its properties
        >>> config.getSettings().zoom
        10.0

    """
    def getSettings(self):
        return getUtility(IGeoSettings)
