collective.geo.settings
=======================

Overview
--------
collective.geo.settings provides some utility to store settings for collective.geo applications.

Tests
-----
in plone registry we have registered some records
    >>> import decimal
    >>> from zope.component import getUtility
    >>> from plone.registry.interfaces import IRegistry
    >>> registry = getUtility(IRegistry)

some settings to provides default values to map widget
    >>> from collective.geo.settings.interfaces import IGeoSettings
    >>> geo_settings = registry.forInterface(IGeoSettings)
    >>> geo_settings
    <RecordsProxy for collective.geo.settings.interfaces.IGeoSettings>

and some settings to provides a default style to geographycal features
    >>> from collective.geo.settings.interfaces import IGeoFeatureStyle
    >>> geo_styles = registry.forInterface(IGeoFeatureStyle)
    >>> geo_styles
    <RecordsProxy for collective.geo.settings.interfaces.IGeoFeatureStyle>

we have registered a coordinate field in IGeoSettings, its store coordinate data as Decimal
    >>> geo_settings.longitude = decimal.Decimal("12.0121210210210")
    >>> geo_settings.longitude
    Decimal('12.0121210210210')

    >>> geo_settings.latitude = decimal.Decimal("13.0999999")
    >>> geo_settings.latitude
    Decimal('13.0999999')
