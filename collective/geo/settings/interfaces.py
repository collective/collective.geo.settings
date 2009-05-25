from zope.interface import Interface
from collective.geo.geopoint.interfaces import IGeoPoint
from zope import schema
from collective.geo.settings import GeoSettingsMessageFactory as _

class IGeoConfig(Interface):
    """ marker interface """

class IGeoSettings(IGeoPoint):
    zoom = schema.Int(title=_(u"Zoom"),
                          description=_(u"Default map's zoom level"),
                          default=None,
                          required=True)

    googlemaps = schema.Bool(title=_(u"Use Google maps layer?"),
                          description=_(u"Check if you want to use google maps layer"),
                          default=False,
                          required=False)

    googleapi = schema.TextLine(title=_(u"Google API Code"),
                          description=_(u"Set google api code if you want use google maps layer"),
                          default=None,
                          required=False)
