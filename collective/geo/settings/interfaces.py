from zope.interface import Interface
from collective.geo.geopoint.interfaces import IGeoPoint
from zope import schema
from collective.geo.settings import GeoSettingsMessageFactory as _

class IGeoConfig(Interface):
    """ marker interface """

class IGeoSettings(IGeoPoint):
    zoom = schema.Float(title=_(u"Zoom"),
                          description=_(u"Default map's zoom level"),
                          default=10.0,
                          required=True)

    googlemaps = schema.Bool(title=_(u"Use Google maps layer?"),
                          description=_(u"Check if you want to use google maps layer"),
                          default=False,
                          required=False)

    googleapi = schema.TextLine(title=_(u"Google API Code"),
                          description=_(u"Set google api code if you want use google maps layer"),
                          default=None,
                          required=False)

class IGeoContainerConfig(Interface):
    """ marker interface """

class IGeoContainerSettings(IGeoPoint):
    """ 
        This interface applies on a per-content (folder/Collection)
        basis, rather than site wide. 
    """
    zoom = schema.Float(title=_(u"Zoom"),
                          description=_(u"Set the zoom level for the view of this container."),
                          default=10.0,
                          required=True)

    googlemaps = schema.Bool(title=_(u"Use Google maps layer?"),
                          description=_(u"Select if you want to use the Google maps layer for the view of this container."),
                          default=False,
                          required=False)

    use_custom_settings = schema.Bool(title=_(u"Use custom view settings"),
                         description=_(u"Select this if you want to use the specified settings on the KML OpenLayers view for this container.  This overrides any defaults set at the site level."),
                         default=False,
                         required=False)
