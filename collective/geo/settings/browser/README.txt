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
