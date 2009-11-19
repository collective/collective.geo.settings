from zope.interface import Interface
from zope.interface.common.mapping import IEnumerableMapping
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

class IMapWidget(Interface):
    """
    Provides configuration options for a specific map widget.
    """

class IMaps(IEnumerableMapping):
    """A mapping form mapids to IMapWidgets

    looked up as ((view, request, context), IMaps)
    """

class IMapView(Interface):
    """
    A view implementing this interface provides configurable
    map widgets.
    """

    mapwidgets = schema.Object(
        title=_('Map Widgets'),
        description=_('A mapping from mapids to IMapWidgets'),
        schema=IMaps)

class IMapLayers(Interface):
    """
    A list of ILayer instances

    specific for ITmapWidget... looked up as ((view, request, context, mapwidget), name)
    """

class IMapLayer(Interface):
    """
    A pluggable interface making it easier to configure layers.
    """

    jsfactory = schema.Text(title=_(u"Javascrpit factory"),
                            description=_(u"Javascript code which returns a new instance of this layer and does not expect any parameters"),
                            required=True)

