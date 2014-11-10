Introduction
============

collective.geo.settings provides some utility to store settings of `collective.geo`_ packages.

.. image:: https://secure.travis-ci.org/collective/collective.geo.settings.png
    :target: http://travis-ci.org/collective/collective.geo.settings

Found a bug? Please, use the `issue tracker`_.

.. contents:: Table of contents


Requirements
============

* `Plone`_ >= 4
* `plone.app.registry`_

Installation
============

This addon can be installed has any other addons, please follow official
documentation_.


Upgrading
=========


General steps
-------------

If you are upgrading from an older version (see below), you may need to run
upgrade steps. To do this, follow these steps:

#. Browse to ``portal_setup`` in the ZMI of your site
#. Click onto the ``Upgrades`` tab
#. Select ``collective.geo.settings:default`` from the drop-down list and
   click ``Choose Profile``
#. Observe any available upgrades and click the ``Upgrade`` button if any
   are present.


Version 0.2.2 and below
-----------------------

New configuration to be added to the portal configuration registry
(``plone.app.registry``) requires an upgrade step to be run.  If you encounter
errors like this::

    Module collective.geo.settings.utils, line 8, in geo_settings
    Module plone.registry.registry, line 74, in forInterface
    KeyError: 'Interface `collective.geo.settings.interfaces.IGeoSettings` defines a field `map_viewlet_managers`, for which there is no record.'

you need to run the relevant upgrade step(s).


Contributors
============

* Giorgio Borelli - gborelli
* Silvio Tomatis - silviot
* David Beitey - davidjb
* Gerhard Weis - gweis
* Rob Gietema - robgietema
* TsungWei Hu - l34marr
* Leonardo J. Caballero G - macagua
* Denis Krienbühl - href


.. _collective.geo: http://plone.org/products/collective.geo
.. _Plone: http://plone.org
.. _plone.app.registry: http://pypi.python.org/pypi/plone.app.registry
.. _issue tracker: https://github.com/collective/collective.geo.bundle/issues
.. _documentation: http://plone.org/documentation/kb/installing-add-ons-quick-how-to
