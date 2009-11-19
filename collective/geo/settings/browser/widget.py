
from zope.interface import implements
from zope.component import getMultiAdapter, getUtility

from Products.Five import BrowserView

from collective.geo.settings.interfaces import IMaps, IMapWidget, IGeoSettings, IMapLayer, IMapLayers

class GeoSettingsMapView(BrowserView):

    # TODO: turn this into descriptor?
    @property
    def mapwidgets(self):
        return getMultiAdapter((self.context, self.request, self.context.context), IMaps)

class MapWidgets(dict):

    implements(IMaps)

    def __init__(self, view, request, context):
        self.view = view
        self.request = request
        self.context = context
        mapfields = getattr(view, 'mapfields', None)
        if mapfields:
            for mapid in mapfields:
                # TODO: if self[mapid] is already IMapWidget (not string) .. then do nothing
                self[mapid] = getMultiAdapter((self.view, self.request, self.context), IMapWidget, name=mapid)
        else:
            self['default-cgmap'] = getMultiAdapter((self.view, self.request, self.context), IMapWidget, name='default-cgmap')

class MapWidget(object):

    implements(IMapWidget)

    mapid = 'default-cgmap'
    klass = 'widget-cgmap'
    style = "witdh:100%;height:450px;"
    js = "// default"
    _layers = []

    def __init__(self, view, request, context):
        self.view = view
        self.request = request
        self.context = context

    @property
    def layers(self):
        return getMultiAdapter((self.view, self.request, self.context, self), IMapLayers)


# var tmslayername = '%s';
# cgmap.extendconfig({
#   'layers': [ function() { return new OpenLayers.Layer.TMS(
#                          tmslayername, '%s',
#                          {type: 'png',
#                           getURL: cgmap.overlay_getTileURL,
#                           alpha: true,
#                           isBaseLayer: false,
#                           visibility: false,
#                           opacity: 0.7
#                          })}]}, 'default-map');
#                         """

    def addClass(self, klass):
        if not self.klass:
            self.klass = unicode(klass)
        else:
            # Make sure items are not repeated.
            parts = self.klass.split() + [unicode(klass)]
            self.klass = u' '.join(frozenset(parts))

class MapLayers(dict):

    implements(IMapLayers)

    def __init__(self, view, request, context, widget):
        self.view = view
        self.request = request
        self.context = context
        self.widget = widget

    def layers(self):
        # shall I use getAllAdapters instead of getNamed?
        layers = []
        useDefaultLayers = getattr(self.widget, 'usedefault', True)
        if useDefaultLayers:
            geosettings = getUtility(IGeoSettings)
            layers.append(geosettings.layers['osm'])
            if geosettings.googlemaps:
                for layername in ('gmap', 'gsat', 'ghyb', 'gter'):
                    layers.append(geosettings.layers[layername])
            if geosettings.yahoomaps:
                for layername in ('ymap', 'ysat', 'yhyb'):
                    layers.append(geosettings.layers[layername])
            if geosettings.bingmaps:
                for layername in ('bmap', 'brod', 'baer', 'bhyb'):
                    layers.append(geosettings.layers[layername])
        maplayers = getattr(self.widget, '_layers', None)
        if maplayers:
            for layerid in maplayers:
                # TODO: if self[layerid] is already ILayer (not string) .. then do nothing
                layers.append(getMultiAdapter((self.view, self.request, self.context, self.widget), IMapLayer, name=layerid))
        return layers

    @property
    def js(self):
        layers = self.layers()
        return "cgmap.extendconfig({layers: [" +\
               ",\n".join([l.jsfactory for l in layers]) + \
               "]}, '%s');" % (self.widget.mapid) 

class MapLayer(object):

    def __init__(self, view, request, context, widget):
        self.view = view
        self.request = request
        self.context = context
        self.widget = widget

    implements(IMapLayer)

    jsfactory = ""
