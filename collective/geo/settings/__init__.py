from zope.i18nmessageid import MessageFactory
import config

GeoSettingsMessageFactory = MessageFactory(config.PROJECTNAME)

_ = GeoSettingsMessageFactory

DISPLAY_PROPERTIES = [('id', _(u'ID')),
                      ('Title', _(u'Title')),
                      ('Description', _(u'Description')),
                      ('Type', _(u'Type')),
                      ('Subject', _(u'Subject')),
                      ('getLocation', _(u'Content Location')),
                      ('ModificationDate', _(u'Last Modified Date')),
                      ('CreationDate', _(u'Creation Date')),
                      ('EffectiveDate', _(u'Effective Date')),
                      ('ExpirationDate', _(u'Expiration Date')),
                      ('listCreators', _(u'Creators')),
                      ('Contributors', _(u'Contributors')),
                      ('Rights', _(u'Rights Statement'))]

DISPLAY_PROPERTIES_DATES = ('ModificationDate',
                         'CreationDate',
                         'EffectiveDate',
                         'ExpirationDate')
