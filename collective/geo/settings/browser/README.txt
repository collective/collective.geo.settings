collective.geo.settings.browser
===============================

Overview
--------

this package provides some handy page macros and adapters t easily manage
multiple maps on one page.

Tests
-----

we start the tests with the usual boilerplate
    >>> from Products.Five.testbrowser import Browser
    >>> browser = Browser()
    >>> portal_url = self.portal.absolute_url()
    >>> self.portal.error_log._ignored_exceptions = ()
    >>> from Products.PloneTestCase.setup import portal_owner, default_password
    >>> browser.open(portal_url)

