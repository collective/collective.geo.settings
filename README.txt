collective.geo.settings
=======================

.. contents:: Summary
   :local:

Introduction
------------

collective.geo.settings provides some utility to store settings of collective.geo packages.

Requirements
------------
* Plone >= 4
* plone.app.registry

Installation
------------
You can install collective.geo.settings as part of a specific project's buildout, by having a buildout configuration such as: ::

        [buildout]
        ...
        eggs = 
            collective.geo.settings
        ...
        [instance]
        ...
        zcml = 
            collective.geo.settings

Install this product from the Plone control panel.


Contributors
------------

* Giorgio Borelli - gborelli
* Silvio Tomatis - silviot
* David Breitkreutz - rockdj
* Gerhard Weis - gweis
