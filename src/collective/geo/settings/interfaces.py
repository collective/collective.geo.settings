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
        description=_(
            u"Choose which content types "
            u"(e.g. Page, News Item, etc) "
            u"can be georeferenced. "
            u"Be aware that, "
            u"when you change this setting, "
            u"the system might take quite some time to apply it "
            u"to the whole site, "
            u"especially if you have many objects within it."
        ),
        value_type=schema.Choice(
            title=_(u"Content types"),
            vocabulary="collective.geo.attypesvocabulary"
        )
    )

    default_layers = schema.List(
        title=_(u'Default map layers'),
        required=False,
        default=[],
        description=_(
            u"Choose which layers will be activated on the map layout."
        ),
        value_type=schema.TextLine(title=u"Layers"))

    longitude = Coordinate(
        title=_(u'Longitude'),
        default=decimal.Decimal("0.0"),
        required=True)

    latitude = Coordinate(
        title=_(u'Latitude'),
        default=decimal.Decimal("0.0"),
        required=True)

    zoom = schema.Decimal(
        title=_(u"Zoom"),
        default=decimal.Decimal("10.0"),
        required=True)

    imgpath = schema.TextLine(
        title=_(u"OpenLayers theme"),
        description=_(
            u"Provide the base path of the OpenLayers theme. "
            u"You can use an absolute URL or a TAL expression."
        ),
        default=u"string:${portal_url}/img/",
        required=False
    )

    googleapi = schema.TextLine(
        title=_(u"Google API Code"),
        description=_(
            u"Provide the Google API code "
            u"if you want to use the Google Maps layer."
        ),
        default=u"ABQIAAAAaKes6QWqobpCx2AOamo-shTwM0brOpm-"
                u"All5BF6PoaKBxRWWERSUWbHs4SIAMkeC1KV98E2EdJKuJw",
        required=False)

    bingapi = schema.TextLine(
        title=_(u"Bing API Code"),
        description=_(
            u"Provide the Bing API code "
            u"if you want to use the Bing Maps layer."
        ),
        default=u"YOUR_API_KEY",
        required=False)

    map_viewlet_managers = schema.List(
        title=_(u'Viewlet managers'),
        required=False,
        default=[],
        description=_(
            u"Specify which viewlet manager can contain "
            u"the map displayed on the georeferenced content view. "
            u"Insert them one per line, "
            u"where each line has the 'dotted name|title' format."
            u"If you want to insert a new viewlet manager, "
            u"you first have to make sure that the map viewlet "
            u"('collective.geo.kml.browser.viewlets.ContentViewlet') "
            u"is registered for that manager (via ZCML)."
        ),
        value_type=schema.TextLine(title=u"Viewlet manager"))


class IGeoFeatureStyle(Interface):
    """IGeoFeatureStyle
       describe some properties used to display different
       features in the map widgets
    """

    map_viewlet_position = schema.Choice(
        title=_(u"Map position"),
        description=_(
            u"Choose if and where the map will be displayed "
            u"within the georeferenced content view."
        ),
        vocabulary='mapviewletmanagersVocab',
        default='plone.abovecontentbody',
        required=True)

    map_width = schema.TextLine(
        title=_(u"Map width"),
        description=_(
            u"Choose the width of the displayed map, "
            u"specified as an absolute value (e.g. '450px' or '15em'), "
            u"or relative (e.g. '100%') size."
        ),
        required=False)

    map_height = schema.TextLine(
        title=_(u"Map height"),
        description=_(
            u"Choose the height of the displayed map, "
            u"specified as an absolute value (e.g. '450px' or '15em'), "
            u"or relative (e.g. '100%') size."
        ),
        required=False)

    linecolor = schema.TextLine(
        title=_(u"Line color"),
        description=_(
            u"Choose the color for the line feature"
        ),
        default=u'ff00003c',
        required=True)

    linewidth = schema.Float(
        title=_(u"Line width"),
        description=_(u"Choose the width of the line feature"),
        default=2.0,
        required=True)

    polygoncolor = schema.TextLine(
        title=_(u"Polygon color"),
        description=_(u"Choose the color for the polygon feature"),
        default=u'ff00003c',
        required=True)

    marker_image = schema.TextLine(
        title=_(u"Marker image"),
        description=_(
            u"The path to the image used as marker in maps. "
            u"You can use either an absolute URL "
            u"or a TAL expression."
        ),
        default=u'string:${portal_url}/img/marker.png',
        required=True)

    marker_image_size = schema.Float(
        title=_(u"Marker image size"),
        description=_(
            u"Choose the scaling factor "
            u"of the marker shown on maps."
        ),
        default=0.7,
        required=True)

    display_properties = schema.List(
        title=_(u"Balloon details"),
        description=_(
            u"Choose which properties "
            u"of the georeferenced content "
            u"will be displayed "
            u"in the additional informations section "
            u"of the balloon."
        ),
        required=False,
        value_type=schema.Choice(
            vocabulary='displaypropertiesVocab'),
        default=['Title', 'Description']
    )

    balloonstyle = schema.TextLine(
        title=_(u"Balloon style"),
        description=_(u"Text displayed in the balloon."),
        default=u'<h2>$[name]</h2>$[description]',
        required=True)


class IGeoCustomFeatureStyle(IGeoFeatureStyle):
    """IGeoCustomFeatureStyle
       describe some properties used to display different
       features in the map widgets per content type
    """

    use_custom_styles = schema.Bool(
        title=_(u"Use custom styles?"),
        description=_(
            u"Check this option if you want to "
            u"customize the style of the geo features for this content"
        ),
        default=False)
