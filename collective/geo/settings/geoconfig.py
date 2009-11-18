from persistent import Persistent
from zope.interface import implements
from zope.component import getUtility
from zope.annotation.interfaces import IAnnotations
from persistent.dict import PersistentDict

from collective.geo.settings.interfaces import IGeoSettings, IGeoContainerSettings
from collective.geo.settings.config import KEY
from collective.geo.settings.event import GeoContainerSettingsModifiedEvent

from Products.CMFCore.utils import getToolByName

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
    """ Manage container-specific settings that may get applied """
    implements(IGeoContainerSettings)

    def __init__(self, context=None, form=None):
        self.context = context
        self.form = form

        if self.context is not None:
            #get our site's config to set the default values from it
            portal_url = getToolByName(self.context, 'portal_url')
            portal = portal_url.getPortalObject()
            self.siteconfig = IGeoSettings(portal)
        else:
            self.siteconfig = None

    def initialiseSettings(self, context):
        annotations = IAnnotations(context)
        self.geo = annotations.get(KEY, None)

        if self.geo is None:
            annotations[KEY] = PersistentDict()
            self.geo = annotations[KEY]

        if not self.geo.has_key('container_settings'):
            self.geo['container_settings'] = {}
            self.geo_container_settings = self.geo['container_settings']
            self.geo_container_settings['use_custom_settings'] = False

            if self.siteconfig is not None:
                self.geo_container_settings['longitude'] = self.siteconfig.longitude
                self.geo_container_settings['latitude'] = self.siteconfig.latitude
                self.geo_container_settings['zoom'] = self.siteconfig.zoom
                self.geo_container_settings['googlemaps'] = self.siteconfig.googlemaps
            else:
                self.geo_container_settings['longitude'] = 7.68047
                self.geo_container_settings['latitude'] = 45.682143
                self.geo_container_settings['zoom'] = 10.0 
                self.geo_container_settings['googlemaps'] = True

    #Watch out here, since we're modifying our dictionary.
    #Set the 'dirty bit' manually here as per
    #http://docs.zope.org/zodb/zodbguide/prog-zodb.html#modifying-mutable-objects
    def set(self, key,  val):
        self.geo['container_settings'][key] = val
        self.geo._p_changed = True

    def getSettings(self, context):
        self.initialiseSettings(context)
        return self.geo['container_settings']

    def get(self, key,  default=False):
        try:
            return self.geo['container_settings'].get(key)
        except:
            return default


