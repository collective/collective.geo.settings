from zope.i18nmessageid import MessageFactory
import config

GeoSettingsMessageFactory = MessageFactory(config.PROJECTNAME)

def initialize(context):
    """Initializer called when used as a Zope 2 product."""


from zope.component.interfaces import ComponentLookupError
from collective.geo.settings.geoconfig import GeoContainerSettings 
from plone.indexer.decorator import indexer
from zope import interface

@indexer(interface.Interface)
def zgeo_geometry_settings_value(object):
    try:
        settings = GeoContainerSettings(object)
        return dict(container_settings=settings.getSettings(object))
    except (ComponentLookupError, TypeError, ValueError, KeyError, IndexError):
        # The catalog expects AttributeErrors when a value can't be found
        raise AttributeError

