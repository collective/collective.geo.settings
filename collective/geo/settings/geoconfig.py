from persistent import Persistent
from zope.interface import implements
from collective.geo.settings.interfaces import IGeoSettings, IGeoContainerSettings
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


class GeoContainerSettings(Persistent):
    """ Make our own shortly... """
    implements(IGeoContainerSettings)

    latitude = 45.682143
    longitude = 7.68047
    zoom = 10.0
    googlemaps = True

    def set(self, key,  val):
        return self.__setattr__(key, val)

    def get(self, key,  default=False):
        try:
            return self.__getattribute__(key)
        except:
            return default

class GeoContainerConfig(object):
    """ Make our own shortly
    """
    def getSettings(self):
        return getUtility(IGeoContainerSettings)
