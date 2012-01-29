from zope.interface import implements
from plone.app.controlpanel.interfaces import IConfigurationChangedEvent
from plone.app.controlpanel.events import ConfigurationChangedEvent


class IGeoSettingsEvent(IConfigurationChangedEvent):
    """An event signaling that geo settings are saved
    """


class GeoSettingsEvent(ConfigurationChangedEvent):
    implements(IGeoSettingsEvent)
