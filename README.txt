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

Install this product from the Plone control panel.

Upgrading
---------

General steps
^^^^^^^^^^^^^

If you are upgrading from an older version (see below), you may need to run 
upgrade steps. To do this, follow these steps:

#. Browse to ``portal_setup`` in the ZMI of your site
#. Click onto the ``Upgrades`` tab
#. Select ``collective.geo.settings:default`` from the drop-down list and 
   click ``Choose Profile``
#. Observe any available upgrades and click the ``Upgrade`` button if any
   are present.

Version 0.2.2 and below
^^^^^^^^^^^^^^^^^^^^^^^

New configuration to be added to the portal configuration registry
(``plone.app.registry``) requires an upgrade step to be run.  If you encounter
errors like this::

    Module collective.geo.settings.utils, line 8, in geo_settings
    Module plone.registry.registry, line 74, in forInterface
    KeyError: 'Interface `collective.geo.settings.interfaces.IGeoSettings` defines a field `map_viewlet_managers`, for which there is no record.'

you need to run the relevant upgrade step(s).

Contributors
------------

* Giorgio Borelli - gborelli
* Silvio Tomatis - silviot
* David Beitey (Breitkreutz) - davidjb/rockdj
* Gerhard Weis - gweis
* Rob Gietema, robgietema
* Leonardo J. Caballero G, macagua

