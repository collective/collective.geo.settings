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
    >>> str(config.zoom)
    '10.0'
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

check error handling in main form:
    >>> browser.getControl(name = 'form.widgets.zoom').value = 'aa'
    >>> browser.getControl('Apply').click()
    >>> '<div class="error">' in browser.contents
    True

zoom should be unchanged
    >>> str(config.zoom)
    '10.0'

try it for subforms:
    >>> browser.getControl(name = 'form.widgets.zoom').value = '5.0'
    >>> browser.getControl(name = 'form.widgets.longitude').value = 'aa'
    >>> browser.getControl('Apply').click()
    >>> '<div class="error">' in browser.contents
    True

zoom and longitude should be unchanged
    >>> str(config.zoom)
    '10.0'
    >>> str(config.longitude)
    '7.68047'
