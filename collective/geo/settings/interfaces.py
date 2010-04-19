import decimal
from zope.interface import Interface

from zope import schema

from collective.geo.settings.schema import Coordinate
from collective.geo.settings import GeoSettingsMessageFactory as _


class IGeoSettings(Interface):
    """IGeoSettings base settings for collective.geo
       describe some default properties used to display the map
       widgets in Plone
    """
    longitude = Coordinate(
        title=_(u'Longitude'),
        description=_(u""),
        default=decimal.Decimal("0.0"),
        required=True)

    latitude = Coordinate(
        title=_(u'Latitude'),
        description=_(u""),
        default=decimal.Decimal("0.0"),
        required=True)

    zoom = schema.Decimal(
        title=_(u"Zoom"),
        description=_(u"Default map's zoom level"),
        default=decimal.Decimal("10.0"),
        required=True)

    googlemaps = schema.Bool(
        title=_(u"Use Google maps layer?"),
        description=_(u"Check if you want to use Google maps layer"),
        default=True,
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


class IGeoFeatureStyle(Interface):
    """IGeoFeatureStyle
       describe some properties used to display different
       features in the map widgets
    """

    linecolor = schema.TextLine(title=_(u"Line color"),
                          description=_(u"Default line color"),
                          default=u'#ff0000',
                          required=True)

    linewidth = schema.Float(title=_(u"Line width"),
                          description=_(u"Default line width in pixels"),
                          default=2.0,
                          required=True)

    polygoncolor = schema.TextLine(title=_(u"Polygon color"),
                          description=_(u"Default polygon color"),
                          default=u'#ff0000',
                          required=False)

    marker_image = schema.TextLine(title=_(u"Marker image"),
                          description=_(u"Default point marker image"),
                          default=u'img/marker.png',
                          required=False)

    marker_image_size = schema.Float(title=_(u"Marker image size"),
                          description=_(u"Scaled size of the marker image"),
                          default=0.7,
                          required=True)

    # display_properties = schema.List(title=_(u"Properties to display"),
    #                       description=_(u"Select what aspects you would "
    #                                       "like to display to the user."),
    #                       required=False,
    #                       value_type=schema.Choice(
    #                                       vocabulary=DISPLAY_VOCABULARY)
    #                       )
