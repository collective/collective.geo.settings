from persistent import Persistent
from zope.interface import implements
from collective.geo.settings.interfaces import IGeoSettings
from collective.geo.settings.maplayers import (OSMMapLayer, BingStreetMapLayer, BingRoadsMapLayer,
                                               BingAerialMapLayer, BingHybridMapLayer,
                                               GoogleStreetMapLayer, GoogleSatelliteMapLayer,
                                               GoogleHybridMapLayer, GoogleTerrainMapLayer,
                                               YahooStreetMapLayer, YahooSatelliteMapLayer,
                                               YahooHybridMapLayer)
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

        return False for unknown properties
        >>> config.get('notthere')
        False

        check whether the tool returns only activated layers.
        all layers are active by default and the first layer is osm
        >>> len(config.layers)
        12
        >>> config.layers[0].name
        'osm'

        turn off yahoo and bing
        >>> config.yahoomaps = False
        >>> config.bingmaps = False
        >>> len(config.layers)
        5

        if all layers are turned off, there should be at least the osm layer there
        >>> config.googlemaps = False
        >>> len(config.layers)
        1
        >>> config.layers[0].name
        'osm'

    """
    implements(IGeoSettings)

    latitude = 45.682143
    longitude = 7.68047
    zoom = 10.0
    googlemaps = True
    googleapi = 'ABQIAAAAaKes6QWqobpCx2AOamo-shTwM0brOpm-All5BF6PoaKBxRWWERSUWbHs4SIAMkeC1KV98E2EdJKuJw'

    yahoomaps = True # turned off by default ... strange side effects
    yahooapi = 'YOUR_API_KEY' #'qw4md4TV34EcJ2sffsBc8A7W0iNPA866PwmFB2PiYW8lw5W8DQJgFy1sTEw_9.LcJNSDrfxcqA--'

    bingmaps = True # turned off by default

    # TODO: turn this into a Folder (or some sort of btree/dict storage), and manage layers as content objects in this folder
    # TODO: basically this tool imlpements the IMapLayers interface....
    #       shall we mark this out and make it really conform/adaptable to IMapLayers?
    @property
    def layers(self):
        layers = [OSMMapLayer()]
        if self.googlemaps:
            layers.append(GoogleStreetMapLayer())
            layers.append(GoogleSatelliteMapLayer())
            layers.append(GoogleHybridMapLayer())
            layers.append(GoogleTerrainMapLayer())
        if self.yahoomaps:
            layers.append(YahooStreetMapLayer())
            layers.append(YahooSatelliteMapLayer())
            layers.append(YahooHybridMapLayer())
        if self.bingmaps:
            layers.append(BingStreetMapLayer())
            layers.append(BingRoadsMapLayer())
            layers.append(BingAerialMapLayer())
            layers.append(BingHybridMapLayer())
        return layers

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
