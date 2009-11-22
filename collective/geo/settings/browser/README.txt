collective.geo.settings.browser
===============================

Overview
--------

this package provides some handy page macros and adapters t easily manage
multiple maps on one page.

Tests
-----

let's creat a view which should display a map.
    >>> from Products.Five import BrowserView
    >>> class TestView(BrowserView):
    ...    def __call__(self):
    ...        return self.template()

We need a request to instantiate the view
    >>> from zope.publisher.browser import TestRequest
    >>> request = TestRequest()
    >>> view = TestView(self.portal, request)

A small helper method to set the template for a view:
    >>> import os
    >>> from zope.app.pagetemplate import ViewPageTemplateFile
    >>> from zope.app.pagetemplate.viewpagetemplatefile import BoundPageTemplate
    >>> from collective.geo.settings import tests
    >>> def setTemplate(view, filename):
    ...     view.template = BoundPageTemplate(ViewPageTemplateFile(
    ...             filename, os.path.dirname(tests.__file__)), view)

We also need a page template to render
    >>> import tempfile
    >>> template = tempfile.mktemp('text.pt')
    >>> open(template, 'w').write('''<html xmlns="http://www.w3.org/1999/xhtml"
    ...       xmlns:metal="http://xml.zope.org/namespaces/metal">
    ...     <head>
    ...         <metal:use use-macro="context/@@geosettings-macros/openlayers" />
    ...     </head>
    ...     <body>
    ...         <metal:use use-macro="context/@@geosettings-macros/map-widget" />
    ...     </body>
    ... </html>
    ... ''')
    >>> setTemplate(view, template)

Render the view:

We should find the OpenLayers.js, our current default map state with center and
zoom set in the control panel, the map widget with class 'widget-cgmap' and
the layer configuration with ass the active layers for this map.
Once the page is loaded in a browser, the bundled script in geo-settigs.js
looks for elements with class 'widget-cgmap' and uses the configuration in
cgmap.state and cgmap.config to initialise OpenLayers on these elements.

    >>> print view()
    <html xmlns="http://www.w3.org/1999/xhtml">
    ...
          <script type="text/javascript" src="./OpenLayers.js"></script>
    ...
          <script type="text/javascript" src="++resource++geo-settings.js"></script>
    ...
          <script type="text/javascript">cgmap.state = {'default': {lon: 7.680470, lat: 45.682143, zoom: 10 }};</script>
    ...
          <div id="default-cgmap" class="widget-cgmap"
    ...
          <script type="text/javascript">cgmap.extendconfig({layers: [
        function() { return new OpenLayers.Layer.TMS( 'OpenStreetMap',
            'http://tile.openstreetmap.org/',
    ...

Another way to render a map is to define an attribute named 'mapfields' on the
view. This field must be a list or tuple and should contain IMapWidget
instances or just strings (or a mix), which are then used to look up an
IMapWidget in the adapter registry.

Let's add an attribute to the view. We also need to adapt the template
slightly.
    >>> from collective.geo.settings.browser.widget import MapWidget
    >>> mw1 = MapWidget(view, request, self.portal)
    >>> mw1.mapid = 'mymap1'
    >>> mw1.addClass('mymapclass1')
    >>> view.mapfields = [mw1]

Let's examine the result:
    >>> print view()
    <html xmlns="http://www.w3.org/1999/xhtml">
    ...
          <div id="mymap1" class="mymapclass1 widget-cgmap"
               style="witdh:100%;height:450px;">
            <!--   openlayers map     -->
          </div>
          <script type="text/javascript">cgmap.extendconfig({layers: [
        function() { return new OpenLayers.Layer.TMS( 'OpenStreetMap',
            'http://tile.openstreetmap.org/',
    ...

If there is more than one entry in mapfields, then only the first one will be
rendered unless we change the template slightly.

    >>> mw2 = MapWidget(view, request, self.portal)
    >>> mw2.mapid = 'mymap2'
    >>> mw2.addClass('mymapclass2')
    >>> view.mapfields.append(mw2)

Let's examine the result with an unchanged template:
    >>> print view()
    <html xmlns="http://www.w3.org/1999/xhtml">
    ...
          <div id="mymap1" class="mymapclass1 widget-cgmap"
               style="witdh:100%;height:450px;">
            <!--   openlayers map     -->
          </div>
          <script type="text/javascript">cgmap.extendconfig({layers: [
        function() { return new OpenLayers.Layer.TMS( 'OpenStreetMap',
            'http://tile.openstreetmap.org/',
    ...

Adapt the template to get both maps. We can do this in various ways.
To render each map individually we have to iterate the list manually. There is
a small helper view which makes things easier later, so let's use it.

    >>> open(template, 'w').write('''<html xmlns="http://www.w3.org/1999/xhtml"
    ...       xmlns:metal="http://xml.zope.org/namespaces/metal">
    ...     <head>
    ...         <metal:use use-macro="context/@@geosettings-macros/openlayers" />
    ...     </head>
    ...     <body>
    ...         <tal:omit tal:define="maps context/@@geosettings-maps/mapwidgets" tal:omit-tag="">
    ...             <tal:omit tal:define="cgmap maps/mymap1" tal:omit-tag="">
    ...                 <metal:use use-macro="context/@@geosettings-macros/map-widget" />
    ...             </tal:omit>
    ...             <tal:omit tal:define="cgmap maps/mymap2" tal:omit-tag="">
    ...                 <metal:use use-macro="context/@@geosettings-macros/map-widget" />
    ...             </tal:omit>
    ...         </tal:omit>
    ...     </body>
    ... </html>
    ... ''')
    >>> setTemplate(view, template)

Let's see what happens:
    >>> print view()
    <html xmlns="http://www.w3.org/1999/xhtml">
    ...
          <div id="mymap1" class="mymapclass1 widget-cgmap"
               style="witdh:100%;height:450px;">
            <!--   openlayers map     -->
          </div>
          <script type="text/javascript">cgmap.extendconfig({layers: [
        function() { return new OpenLayers.Layer.TMS( 'OpenStreetMap',
            'http://tile.openstreetmap.org/',
    ...
          <div id="mymap2" class="mymapclass2 widget-cgmap"
               style="witdh:100%;height:450px;">
            <!--   openlayers map     -->
          </div>
          <script type="text/javascript">cgmap.extendconfig({layers: [
        function() { return new OpenLayers.Layer.TMS( 'OpenStreetMap',
            'http://tile.openstreetmap.org/',
    ...

We can also just iterate over the mapwidgets list:
    >>> open(template, 'w').write('''<html xmlns="http://www.w3.org/1999/xhtml"
    ...       xmlns:metal="http://xml.zope.org/namespaces/metal">
    ...     <head>
    ...         <metal:use use-macro="context/@@geosettings-macros/openlayers" />
    ...     </head>
    ...     <body>
    ...         <tal:omit tal:repeat="cgmap context/@@geosettings-maps/mapwidgets" tal:omit-tag="">
    ...             <metal:use use-macro="context/@@geosettings-macros/map-widget" />
    ...         </tal:omit>
    ...     </body>
    ... </html>
    ... ''')
    >>> setTemplate(view, template)

As our first template was not very sophisticated, we should get the same
result:
    >>> print view()
    <html xmlns="http://www.w3.org/1999/xhtml">
    ...
          <div id="mymap1" class="mymapclass1 widget-cgmap"
               style="witdh:100%;height:450px;">
            <!--   openlayers map     -->
          </div>
          <script type="text/javascript">cgmap.extendconfig({layers: [
        function() { return new OpenLayers.Layer.TMS( 'OpenStreetMap',
            'http://tile.openstreetmap.org/',
    ...
          <div id="mymap2" class="mymapclass2 widget-cgmap"
               style="witdh:100%;height:450px;">
            <!--   openlayers map     -->
          </div>
          <script type="text/javascript">cgmap.extendconfig({layers: [
        function() { return new OpenLayers.Layer.TMS( 'OpenStreetMap',
            'http://tile.openstreetmap.org/',
    ...

It is also possible to register an IMapWidget as named adapter and just give
it's name in mapfields. IMapMidgets are looked up by ((view, request, context),
name). So let's update our configuraion and fields:

    >>> def mw1factory(view, request, context):
    ...     mw = MapWidget(view, request, context)
    ...     mw.mapid = 'mymap1'
    ...     mw.addClass('mymapclass1')
    ...     return mw
    >>> from zope.component import provideAdapter
    >>> from zope.interface import Interface
    >>> from collective.geo.settings.interfaces import IMapWidget
    >>> provideAdapter(mw1factory,
    ...                (Interface, Interface, Interface),
    ...                IMapWidget, name='mw1')
    >>> view.mapfields = ['mw1', mw2]
    >>> print view()
    <html xmlns="http://www.w3.org/1999/xhtml">
    ...
          <div id="mymap1" class="mymapclass1 widget-cgmap"
               style="witdh:100%;height:450px;">
            <!--   openlayers map     -->
          </div>
          <script type="text/javascript">cgmap.extendconfig({layers: [
        function() { return new OpenLayers.Layer.TMS( 'OpenStreetMap',
            'http://tile.openstreetmap.org/',
    ...
          <div id="mymap2" class="mymapclass2 widget-cgmap"
               style="witdh:100%;height:450px;">
            <!--   openlayers map     -->
          </div>
          <script type="text/javascript">cgmap.extendconfig({layers: [
        function() { return new OpenLayers.Layer.TMS( 'OpenStreetMap',
            'http://tile.openstreetmap.org/',
    ...

The defaul IMaps implementation complains if an element in mapfields is nat a
string or IMapWidget:

    >>> view.mapfields = ['mw1', mw2, None]
    >>> print view()
    Traceback (most recent call last):
    ...
    ValueError: Can't create IMapWidget for None

Now we have covered the most important things about map midgets. Set us try
some things with map layers.

Layers:
-------

Map widgets can have lyars associated with them. These association is handled
similar to the IMapWidget - View associaton above. An IMapWidget instance has
to provide an attribute 'layers', which is a mapping from layer-id to ILayer
instances. The default IMapWidget implementation provides 'layers' as a
computed attribute. On access it looks up an IMapLayers - manager implementation which
handles the actual IMapLayer instantiation. If the widget has an attribute
'usedefault' and it is set to False, the layer manager ignoles all default
layers set in the controlpanel, else all the default layers are
added. Additionally the map widget can provide an attribute '_layers', which is
a list of names and/or ILayer instances to be added.

As a quick example we can just set the '_layers' attribute for mw1 and we
should get an additional layer.
    >>> from collective.geo.settings.maplayers import BingStreetMapLayer
    >>> mw1._layers = [BingStreetMapLayer()]
    >>> view.mapfields = [mw1]
    >>> print view()
    <html xmlns="http://www.w3.org/1999/xhtml">
    ...
          <div id="mymap1" class="mymapclass1 widget-cgmap"
               style="witdh:100%;height:450px;">
            <!--   openlayers map     -->
          </div>
          <script type="text/javascript">cgmap.extendconfig({layers: [
        function() { return new OpenLayers.Layer.TMS( 'OpenStreetMap',
            'http://tile.openstreetmap.org/',
    ...
        function() { return new OpenLayers.Layer.VirtualEarth('Bing Streets',
    ...

Me can register the BingStreetMapLayer as an adapter which allows us to use
just the name to get the same result. ILayers are looked up for ((view,
request, context, widget), name):

    >>> from collective.geo.settings.interfaces import IMapLayer
    >>> provideAdapter(BingStreetMapLayer,
    ...                (Interface, Interface, Interface, Interface),
    ...                IMapLayer, name='bsm')
    >>> mw1._layers = ['bsm']
    >>> print view()
    <html xmlns="http://www.w3.org/1999/xhtml">
    ...
          <div id="mymap1" class="mymapclass1 widget-cgmap"
               style="witdh:100%;height:450px;">
            <!--   openlayers map     -->
          </div>
          <script type="text/javascript">cgmap.extendconfig({layers: [
        function() { return new OpenLayers.Layer.TMS( 'OpenStreetMap',
            'http://tile.openstreetmap.org/',
    ...
        function() { return new OpenLayers.Layer.VirtualEarth('Bing Streets',
    ...

If _layers contains somethin which can't be converted into an IMapLayer
instance, me get an exception:
    >>> mw1._layers = ['bsm', None]
    >>> print view()
    Traceback (most recent call last):
    ...
    ValueError: Can't create IMapLayer for None


TODO: da a custom IMapLayer class

TODO: demonstrate cgmap.config + cgmap.state

TODO: do some request turn around map_state tests (coverage in GeoSettingsView)

