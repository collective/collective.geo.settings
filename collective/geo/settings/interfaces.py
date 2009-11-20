
import decimal

from zope.interface import Interface
from zope.interface.common.mapping import IEnumerableMapping
from zope import schema

from collective.geo.settings.z3cform import Decimal
from collective.geo.settings import GeoSettingsMessageFactory as _

class IGeoConfig(Interface):
    """ marker interface """
    pass

class IGeoSettings(Interface):
    longitude = Decimal(
        title=_(u'Longitude'),
        description=_(u""),
        default=None,
        required=True)

    latitude  = Decimal(
        title=_(u'Latitude'),
        description=_(u""),
        default=None,
        required=True)

    zoom = Decimal(
        title=_(u"Zoom"),
        description=_(u"Default map's zoom level"),
        default=decimal.Decimal("10.0"),
        required=True)

    googlemaps = schema.Bool(
        title=_(u"Use Google maps layer?"),
        description=_(u"Check if you want to use Google maps layer"),
        default=False,
        required=False)

    googleapi = schema.TextLine(
        title=_(u"Google API Code"),
        description=_(u"Set Google api code if you want use Google maps layer"),
        default=None,
        required=False)

    yahoomaps = schema.Bool(
        title=_(u"Use Yahoo maps layer?"),
        description=_(u"Check if you want to use Yahoo maps layer"),
        default=False,
        required=False)

    yahooapi = schema.TextLine(
        title=_(u"Yahoo API Code"),
        description=_(u"Set Yahoo api code if you want use Yahoo maps layer"),
        default=None,
        required=False)

    bingmaps = schema.Bool(
        title=_(u"Use Bing maps layer?"),
        description=_(u"Check if you want to use Bing maps layer"),
        default=False,
        required=False)

class IMaps(IEnumerableMapping):
    """A mapping form mapids to IMapWidgets

    looked up as ((view, request, context), IMaps)
    """

class IMapLayers(IEnumerableMapping):
    """
    A mapping of IMapLayer instances

    specific for IMapWidget... looked up as ((view, request, context, mapwidget), name)
    """

    js = schema.TextLine(
        title=_(u"Javascript to configure layers."),
        description=_("Returns some js-code to set up available layers."),
        required=True)

class IMapWidget(Interface):
    """
    Provides configuration options for a specific map widget.
    """
    mapid = schema.TextLine(
        title=_(u"Map id"),
        description=_(u"Used to identify the map in the dom-tree and to lookup"\
                      u" an IMapWidget component if necessary."),
        default=u"default-cgmap",
        required=True)

    klass = schema.TextLine(
        title=_(u"Class attribute"),
        description=_(u"The html element class attribute."),
        default=u"widget-cgmap",
        required=True)

    style = schema.TextLine(
        title=_(u"Style attribute"),
        description=_(u"The html element style attribute."),
        required=False)

    js = schema.Text(
        title=_("Javascript extras"),
        description=_(u"Additional Javascript code inserted after the map widget."),
        required=False)

    layers = schema.Object(
        title=_('Layers'),
        description=_('A mapping from layerids to ILayers'),
        schema=IMapLayers)

    usedefault = schema.Bool(
        title=_(u"Enable default layers."),
        description=_(u"If set to true, the default IMapLayers implementation"\
                      u" adds all enabled default layers from the geo settings tool."),
        default=True,
        required=False)

    def addClass(klass):
        '''
        add klass to self.klass
        '''

class IMapView(Interface):
    """
    A view implementing this interface provides configurable
    map widgets.
    """
    # TODO: is this the right field for an IMapView or should it be mapfields here?
    mapwidgets = schema.Object(
        title=_('Map Widgets'),
        description=_('A mapping from mapids to IMapWidgets'),
        schema=IMaps)


class IMapLayer(Interface):
    """
    A pluggable interface making it easier to configure layers.
    """

    jsfactory = schema.Text(
        title=_(u"Javascrpit factory"),
        description=_(u"Javascript code which returns a new instance of this layer"\
                      u" and does not expect any parameters"),
        required=True)
