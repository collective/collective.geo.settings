Introduction
============

collective.geo.settings provides a graphical user interface to store settings of collective.geo packages.

Requirements
------------
* plone >= 3.2.1
* plone.app.z3cform
* collective.geo.openlayers
* collective.geo.geopoint

Installation
============
Just a simple easy_install collective.geo.settings is enough.

Alternatively, buildout users can install collective.geo.settings as part of a specific project's buildout, by having a buildout configuration such as: ::

        [buildout]
        ...
        eggs = 
            zope.i18n>=3.4
            collective.geo.settings
        ...
        [instance]
        ...
        zcml = 
            collective.geo.settings

Install this product from the Plone control panel.


Contributors
============

* Giorgio Borelli - gborelli
* Silvio Tomatis - silviot
* David Breitkreutz - rockdj
