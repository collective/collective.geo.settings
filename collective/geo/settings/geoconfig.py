from persistent import Persistent
from zope.interface import implements
from collective.geo.settings.interfaces import IGeoSettings
from zope.component import getUtility

class GeoSettings(Persistent):
    """ 
        GeoSettings ha un po' di proprieta' cui posso accedere direttamente
        >>> config = GeoSettings()
        >>> config.zoom
        10

        o attraverso il metogo get
        >>> config.get('googlemaps')
        True

        posso anche cambiare le proprieta direttamente
        >>> config.zoom = 9
        >>> config.zoom
        9

        o attraverso il metodo set
        >>> config.set('zoom', 10)
        >>> config.zoom
        10

    """ 
    implements(IGeoSettings)

    latitude = 45.682143
    longitude = 7.68047
    zoom = 10
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
        comunque questa e' la mia utility
        >>> config = GeoConfig()
        >>> config.getSettings()
        <class 'collective.geo.settings.geoconfig.GeoSettings'>

        e queste sono le sue proprieta
        >>> config.getSettings().zoom
        10

    """
    def getSettings(self):
        return getUtility(IGeoSettings)
