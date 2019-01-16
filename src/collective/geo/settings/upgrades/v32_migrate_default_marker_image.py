from collective.geo.settings.interfaces import DEFAULT_IMAGE_LOCATION
from collective.geo.settings.interfaces import DEFAULT_MARKER_LOCATION
from collective.geo.settings.utils import geo_settings
from collective.geo.settings.utils import geo_styles
from plone.registry.interfaces import IRegistry
from zope.component import getUtility
import logging


OLD_DEFAULT_IMAGE_LOCATION = u'string:${portal_url}/img/'
OLD_DEFAULT_MARKER_LOCATION = u'string:${portal_url}/img/marker.png'

def run(context, logger=None):

    if logger is None:
        logger = logging.getLogger('collective.geo.settings')

    # Fix/Set marker_image
    registry = getUtility(IRegistry)
    registry_key_marker_image = 'collective.geo.settings.interfaces.IGeoFeatureStyle.marker_image'
    registry._records._fields[registry_key_marker_image].default = DEFAULT_MARKER_LOCATION

    styles_settings = geo_styles()
    marker_image = styles_settings.marker_image
    if marker_image == OLD_DEFAULT_MARKER_LOCATION or not marker_image:
        styles_settings.marker_image = DEFAULT_MARKER_LOCATION


    # Fix set imgpath
    registry_key_location_images = 'collective.geo.settings.interfaces.IGeoFeatureStyle.marker_image'
    registry._records._fields[registry_key_location_images].default = DEFAULT_IMAGE_LOCATION

    general_settings = geo_settings()
    img_path = general_settings.imgpath
    if img_path == OLD_DEFAULT_IMAGE_LOCATION or not img_path:
        general_settings.imgpath = DEFAULT_IMAGE_LOCATION

    logger.info('New default value for registry field "marker_image" and '
                '"imgpath" has been set')
