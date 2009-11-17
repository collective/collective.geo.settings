collective.geo.settings
=======================

Overview
--------
collective.geo.settings provides a graphical user interface to store settings for collective.geo applications.

Tests
-----
we start the tests with the usual boilerplate
    >>> from Products.Five.testbrowser import Browser
    >>> browser = Browser()
    >>> portal_url = self.portal.absolute_url()
    >>> self.portal.error_log._ignored_exceptions = ()

    >>> from Products.PloneTestCase.setup import portal_owner, default_password
    >>> browser.open(portal_url)

verifiy the registration of the configuration utility
    >>> import zope.component
    >>> from collective.geo.settings.interfaces import IGeoSettings
    >>> config = zope.component.getUtility(IGeoSettings)
    >>> config
    <collective.geo.settings.geoconfig.GeoSettings object ...>

we get some properties in that utility
    >>> config.zoom
    10.0
    >>> config.googlemaps
    True

we log in and verify the functionality of collective.geo.settings control panel form;
    >>> browser.getControl(name='__ac_name').value = portal_owner
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()
    >>> browser.open('%s/@@geosettings-controlpanel' % portal_url)
    >>> browser.getControl(name = 'form.widgets.zoom').value
    '10.0'

we set 'use google maps' property to 'No' and save data
    >>> browser.getControl(name = 'form.widgets.googlemaps:list').value = ['false']
    >>> browser.getControl('Apply').click()

Check that there weren't any errors

    >>> '<div class="error">' in browser.contents
    False

and check the modifications in the configuration utility
    >>> config.googlemaps
    False

Tests on a KML view Folder
--------------------------

Modify a given container and check to see if we're looking at an event

<Modify container here>

Check that an event was generated

from zope.component.eventtesting import getEvents
from zope.lifecycleevent.interfaces import IObjectModifiedEvent
events = getEvents(IObjectModifiedEvent)
len(events)
1
events[0].object is placemark
True

Tests on a KML view Collection
------------------------------


