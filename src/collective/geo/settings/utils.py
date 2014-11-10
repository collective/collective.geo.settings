from zope.component import getUtility

from plone.registry.interfaces import IRegistry
from collective.geo.settings.interfaces import IGeoSettings, IGeoFeatureStyle


def geo_settings(context=None):  # pylint: disable=W0613
    return getUtility(IRegistry).forInterface(IGeoSettings)


def geo_styles(context=None):  # pylint: disable=W0613
    return getUtility(IRegistry).forInterface(IGeoFeatureStyle)
