from zope.interface import implements
from zope.lifecycleevent.interfaces import IObjectModifiedEvent

def reindexContainerSettingsSubscriber(event):
    """A subscriber to ObjectModifiedEvent"""
    event.object.reindexObject()

class IGeoContainerSettingsModifiedEvent(IObjectModifiedEvent):
    """An event signaling that a container's geo settings were modified
    """

class GeoContainerSettingsModifiedEvent(object):
    implements(IGeoContainerSettingsModifiedEvent)

    def __init__(self, ob):
        self.object = ob

