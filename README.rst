Introduction
============

collective.geo.settings provides some utility to store settings of `collective.geo`_ packages.


.. contents:: Table of contents


Requirements
============

* `Plone`_ >= 4
* `plone.app.registry`_


Documentation
=============

Full documentation for end users can be found in the "docs" folder.
It is also available online at https://collectivegeo.readthedocs.io/


Translations
============

This product has been translated into

- Danish.

- German.

- Spanish.

- French.

- Italian.

- Dutch.

- Brazil Portuguese.

- Chinese Simplified.

- Traditional Chinese.

You can contribute for any message missing or other new languages, join us at 
`Plone Collective Team <https://www.transifex.com/plone/plone-collective/>`_ 
into *Transifex.net* service with all world Plone translators community.


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


Tests status
============

This add-on is tested using Travis CI. The current status of the add-on is:

.. image:: https://img.shields.io/travis/collective/collective.geo.settings/master.svg
    :target: http://travis-ci.org/collective/collective.geo.settings

.. image:: http://img.shields.io/pypi/v/collective.geo.settings.svg
   :target: https://pypi.org/project/collective.geo.settings


Contribute
==========

Have an idea? Found a bug? Let us know by `opening a ticket`_.

- Issue Tracker: https://github.com/collective/collective.geo.settings/issues
- Source Code: https://github.com/collective/collective.geo.settings
- Documentation: https://collectivegeo.readthedocs.io/


Contributors
============

* Giorgio Borelli - gborelli
* Silvio Tomatis - silviot
* David Beitey - davidjb
* Gerhard Weis - gweis
* Rob Gietema - robgietema
* TsungWei Hu - l34marr
* Leonardo J. Caballero G. - macagua
* Denis Krienbühl - href


License
=======

The project is licensed under the GPL.

.. _collective.geo: https://pypi.org/project/collective.geo.bundle/
.. _Plone: http://plone.org
.. _plone.app.registry: https://pypi.org/project/plone.app.registry/
.. _`opening a ticket`: https://github.com/collective/collective.geo.bundle/issues
.. _documentation: https://docs.plone.org/manage/installing/installing_addons.html
