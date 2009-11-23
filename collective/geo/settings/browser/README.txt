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

Let's create a custom layer. A rather common use-case may be to display a
static image on a map. Let's assume our context is an Image object in Plone
(e.g. ATImage), and we want an Openlayers view with the Image as base-layer.
(I did not test whether this layer really works with OL, it should rather
demonstrate the concept). MapWidgets also support a 'js' attribute to render
additional java-script if necessary.

    >>> from collective.geo.settings.browser.widget import MapLayer
    >>> class ImageLayer(MapLayer):
    ...     name = "imagelayer"
    ...
    ...     @property
    ...     def jsfactory(self):
    ...         return """
    ...         function() { return new OpenLayers.Layer.Image('%s', {url: '%s'});}
    ...         """ % (self.context.Title(), self.context.absolute_url())

An 'Image Layer' is a rather generic component, so it might be useful to
register it as an adapter. (Probably just for IATImage context objects?)
    >>> provideAdapter(ImageLayer,
    ...                (Interface, Interface, Interface, Interface),
    ...                IMapLayer, name='image')

As this becomes an unprojected base layer we don't want the default base layers
    >>> mw1.usedefault = False
    >>> mw1._layers = ['image']
    >>> mw1.js = "\n// a place to add additional js\n"
    >>> print view()
    <html xmlns="http://www.w3.org/1999/xhtml">
    ...
          <div id="mymap1" class="mymapclass1 widget-cgmap"
               style="witdh:100%;height:450px;">
            <!--   openlayers map     -->
          </div>
          <script type="text/javascript">cgmap.extendconfig({layers: [
            function() { return new OpenLayers.Layer.Image('Plone site', {url: 'http://nohost/plone'});}
            ]}, 'mymap1');</script>
          <script type="text/javascript">
    // a place to add additional js
    </script>
    ...

More fancy things cam be done by turning _layers into a computed property. This
way it is possible to return only those layers of current interest. It is also
possible to register a different IMapLayers instance, which uses some other
algorithm to find all default and custom layers.

Javascript Notes:
-----------------

The Javascript in this package uses jquery to initialise all maps on the
page. This means, that the actual map initalisation is deffered by
jquery(decument).ready calls.

The steps to initialise a map are the following:

  1. find all elements with class widget-cgmap and get their id's
  2. use these id's to find configuration in cgmap.config
  3. use these id's to find state in cgmap.state
  4. create the OpenLayers instance on these elements.

JS Configuration:

  cgmap.config is an object containing the following inormation:

    - cgmap.config['default']: is an object which holds various default
      configurations which are used as fallback if there are no specific
      options for a map. Currently it has an attribute 'options' which is
      directly passed into the OpneLayers constructor and halsd values for
      projection, displayProjection, controls, etc... (see geo-settings.js for
      details)

    - cgmap.config[mapid]: It is possible to set map specic options for each
      map with id mapid. The attribute 'options' is used as options parameter
      and all missing values will be taken form the 'default' options object.
      A good place to customise these values il probably the 'js' field in an
      IMapWidget instance.

  Map object access:

    After the maps hve been initialised, the map-instance object is accessible
    as: cgmap.config[mapid].map


  There is also a helper method in the cgmap namespace which takes of
  generating the cgmap.config object if it does not exist yet:

    - cgmap.extendconfig( {<the actual config data}, 'mapid' )

  cgmap.state is an object which holds state information about a map instance:

    - cgmap.state['default']: is an object which holds zoom, and center lon/lat
      set in the control panel.

    - cgmap.state[mapid]: holds state information for map with id mapid.
      current supported state values are: zoom, conter lon/lat,
      activebaselayer, activelayers (overlays)

  State information for maps is useful in forms, to recreate the same map state
  after a form submit. Therefore the included java-script adds some hidden
  fields to all forms on the page, and the GeosettingsView class extracts these
  values from the request and returns some javascript code to generate the
  necessary data structures

Let's test state passing:

For this we need to adjust the values int the request object. Here we change
the default center lon/lat.

    >>> request.form['cgmap_state_mapids'] = 'mymap1'
    >>> request.form['cgmap_state.mymap1'] = {'lon': 33.33, 'lat': 66.66}
    >>> request.method = 'POST'
    >>> view.context.REQUEST = request
    >>> print view()
    <html xmlns="http://www.w3.org/1999/xhtml">
    ...
          <script type="text/javascript">cgmap.state = {'default': {lon: 7.680470, lat: 45.682143, zoom: 10 }};
    cgmap.state['mymap1'] = {lon: '33.33', lat: '66.66', zoom: undefined, activebaselayer: undefined, activelayers: undefined };</script>
    ...

And another small test to get a 100% test coverage report:

    >>> mw1.klass = None
    >>> mw1.addClass('myclass')
    >>> mw1.klass
    'myclass'
