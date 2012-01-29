from Products.CMFCore.utils import getToolByName

from collective.geo.settings.config import PROJECTNAME

PROFILE_ID = 'profile-%s:default' % PROJECTNAME


def upgrade_registry(context, logger=None):  # pylint: disable=W0613
    """Re-import the portal configuration registry settings.
    """
    setup = getToolByName(context, 'portal_setup')
    setup.runImportStepFromProfile(PROFILE_ID, 'plone.app.registry')
    return
