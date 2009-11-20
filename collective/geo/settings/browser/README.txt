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

