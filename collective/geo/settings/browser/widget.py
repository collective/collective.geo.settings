
from zope.interface import implements
from zope.component import getMultiAdapter, getUtility

from Products.Five import BrowserView

from collective.geo.settings.interfaces import (IMaps, IMapWidget, IGeoSettings,
                                                IMapLayer, IMapLayers, IMapView)

class GeoSettingsMapView(BrowserView):
    '''
    Helper view to look up mapwidgets for current view and context.
    '''
    # TODO: shall this be a IMapView or the view itself?
    implements(IMapView)

    @property
    def mapwidgets(self):
        return getMultiAdapter((self.context, self.request, self.context.context), IMaps)

class MapWidgets(dict):
    '''
    IMaps adapter which initialises IMapWidgets for current view ad context.
    '''

    implements(IMaps)

    def __init__(self, view, request, context):
        self.view = view
        self.request = request
        self.context = context
        mapfields = getattr(view, 'mapfields', None)
        if mapfields:
            for mapid in mapfields:
                if IMapWidget.providedBy(mapid):
                    # is already a MapWidget, just take it
                    self[mapid.mapid] = mapid
                elif isinstance(mapid, basestring):
                    # is only a name... lookup the widget
                    self[mapid] = getMultiAdapter((self.view, self.request, self.context), IMapWidget, name=mapid)
                else:
                    raise ValueError("Can't create IMapWidget for %s" % repr(mapid))
        else:
            # there are no mapfields let's look up the default widget
            self['default-cgmap'] = getMultiAdapter((self.view, self.request, self.context), IMapWidget, name='default-cgmap')

class MapWidget(object):
    '''
    The default IMapWidget, which also can serve as handy base class.
    '''

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

    def addClass(self, klass):
        if not self.klass:
            self.klass = unicode(klass)
        else:
            # Make sure items are not repeated.
            parts = self.klass.split() + [unicode(klass)]
            self.klass = u' '.join(frozenset(parts))

class MapLayers(dict):
    '''
    The default IMapLayers implementation.

    Checks geo settings tool for enabled layers and adds them if enabled (widget.usedefault).

    TODO: this impl is too tigly copled with the default MapWigdet implementation.
          esp.: it should not look for widget._layers attribute.
    '''

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
            layers.extend(geosettings.layers)
        maplayers = getattr(self.widget, '_layers', None)
        if maplayers:
            for layerid in maplayers:
                if IMapLayer.providedBy(layerid):
                    layers.append(layerid)
                elif isinstance(layerid, basestring):
                    layers.append(getMultiAdapter((self.view, self.request, self.context, self.widget), IMapLayer, name=layerid))
                else:
                    raise ValueError("Can't create IMapLayer for %s" % repr(layerid))
        return layers

    @property
    def js(self):
        layers = self.layers()
        return "cgmap.extendconfig({layers: [" +\
               ",\n".join([l.jsfactory for l in layers]) + \
               "]}, '%s');" % (self.widget.mapid)

class MapLayer(object):
    '''
    An empty IMapLayer implementation, useful as base class.

    MapLayers are named components specific for (view, request, context, widget).
    '''

    def __init__(self, view, request, context, widget):
        self.view = view
        self.request = request
        self.context = context
        self.widget = widget

    implements(IMapLayer)

    jsfactory = ""
