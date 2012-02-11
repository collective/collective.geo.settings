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
    geo_content_types = schema.List(
        title=_(u'Georeferenceable content types'),
        required=False,
        default=[],  # 'Document', 'News', 'Event'],
        description=_(u"A list of types can be geo referenced"),
        value_type=schema.Choice(title=_(u"Content types"),
                source="plone.app.vocabularies.ReallyUserFriendlyTypes"))

    default_layers = schema.List(
        title=_(u'Default map layers'),
        required=False,
        default=[],
        description=_(u"A list of layers used in the default map layout"),
        value_type=schema.TextLine(title=u"Layers"))

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

    imgpath = schema.TextLine(
            title=_(u"OpenLayers images path (Expression)"),
            description=_(u""),
            default=u"string:${portal_url}/img/",
            required=False)

    googleapi = schema.TextLine(
       title=_(u"Google API Code"),
       description=_(u"Set Google api code if you want use Google maps layer"),
       default=u"ABQIAAAAaKes6QWqobpCx2AOamo-shTwM0brOpm-"\
                  "All5BF6PoaKBxRWWERSUWbHs4SIAMkeC1KV98E2EdJKuJw",
       required=False)

    yahooapi = schema.TextLine(
        title=_(u"Yahoo API Code"),
        description=_(u"Set Yahoo api code if you want use Yahoo maps layer"),
        default=u"YOUR_API_KEY",
        required=False)

    map_viewlet_managers = schema.List(
        title=_(u'Viewlet managers'),
        required=False,
        default=[],
        description=_(u"Specify all viewlet manager allowed "\
                "to display the map on the page, one per line."\
                " The required format is name|title"),
        value_type=schema.TextLine(title=u"Viewlet manager"))


class IGeoFeatureStyle(Interface):
    """IGeoFeatureStyle
       describe some properties used to display different
       features in the map widgets
    """

    map_viewlet_position = schema.Choice(
              title=_(u"Map display position"),
              description=_(u"Choose the position of the map in the page."),
              vocabulary='mapviewletmanagersVocab',
              default='plone.abovecontentbody',
              required=True)

    map_width = schema.TextLine(
              title=_(u"Map width"),
              description=_(u"Width for maps, specified as an absolute "
                            "(like '450px' or '15em'), or relative (like "
                            "'100%') size."),
              required=False)

    map_height = schema.TextLine(
              title=_(u"Map height"),
              description=_(u"Height for maps, specified as an absolute "
                            "(like '450px' or '15em'), or relative (like "
                            "'100%') size."),
              required=False)

    linecolor = schema.TextLine(title=_(u"Line color"),
                          description=_(u"Default line color"),
                          default=u'ff00003c',
                          required=True)

    linewidth = schema.Float(title=_(u"Line width"),
                          description=_(u"Default line width in pixels"),
                          default=2.0,
                          required=True)

    polygoncolor = schema.TextLine(title=_(u"Polygon color"),
                          description=_(u"Default polygon color"),
                          default=u'ff00003c',
                          required=True)

    marker_image = schema.TextLine(title=_(u"Marker image (Expression)"),
                          description=_(u"Default point marker image"),
                          default=u'string:${portal_url}/img/marker.png',
                          required=True)

    marker_image_size = schema.Float(title=_(u"Marker image size"),
                          description=_(u"Scaled size of the marker image"),
                          default=0.7,
                          required=True)

    display_properties = schema.List(title=_(u"Properties to display"),
                          description=_(u"Select what aspects you would "
                                          "like to display to the user."),
                          required=False,
                          value_type=schema.Choice(
                                          vocabulary='displaypropertiesVocab'),
                          default=['Title', 'Description'])


class IGeoCustomFeatureStyle(IGeoFeatureStyle):
    """IGeoCustomFeatureStyle
       describe some properties used to display different
       features in the map widgets per content type
    """

    use_custom_styles = schema.Bool(
        title=_(u'Use custom styles?'),
        description=_(u'Check this option if you want to '
              'customize the style of the geo features for this content'),
        default=False)
