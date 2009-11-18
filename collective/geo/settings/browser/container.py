from z3c.form import field, form, subform, button, action, interfaces
from plone.z3cform import z2
from plone.z3cform.layout import wrap_form

from Products.CMFPlone.utils import getToolByName

from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from zope import interface, component
from zope.event import notify
from zope.component import getUtility
from zope.app.pagetemplate import viewpagetemplatefile
from zope.app.component.hooks import getSite

from collective.geo.geopoint.geopointform import GeopointBaseForm
from collective.geo.settings.geoconfig import GeoContainerSettings
from collective.geo.settings.interfaces import IGeoContainerSettings
from collective.geo.settings.browser.interfaces import IGeoContainerSettingsForm
from collective.geo.settings import GeoSettingsMessageFactory as _
from collective.geo.settings.event import GeoContainerSettingsModifiedEvent

class GeopointContainerForm(GeopointBaseForm, subform.EditSubForm):
    component.adapts(interfaces.IEditForm)

    label = u"Select where to centre the OpenLayers view for this container."
    form_name = u"Central view point"

    fields = field.Fields(IGeoContainerSettings).select('longitude', 'latitude')

    def __init__(self, context, request, parent):
       super(GeopointContainerForm, self).__init__(context, request, parent)
       self.parentForm = parent

    def update(self):
        super(GeopointContainerForm, self).update()
        self.updateWidgets()

    def getContent(self):
        '''See interfaces.IForm'''
        return self.parentForm.getContent()


class GeoContainerSettingsForm(form.Form):

    interface.implements(IGeoContainerSettingsForm)

    label = u"Configure Collective Geo Settings for this container/Collection."
    form_name = u"Content-Specific Geo Settings Form"

    template = viewpagetemplatefile.ViewPageTemplateFile('form-with-subforms.pt')
    fields = field.Fields(IGeoContainerSettings).select('zoom', 'googlemaps', 'use_custom_settings')

    message_ok = _(u'Changes saved.')
    message_cancel = _(u'No changes made.')

    level = 1
        
    def __init__(self, context, request):
        super(GeoContainerSettingsForm,self).__init__(context,request)

        self.context = context
        self.containersettings = GeoContainerSettings(self.context)

        portal_url = getToolByName(self.context, 'portal_url')
        portal = portal_url.getPortalObject()
        props_tool = getToolByName(portal, 'portal_properties')
        site_props = getattr(props_tool, 'site_properties')
        self.typesUseViewActionInListings = list(site_props.getProperty('typesUseViewActionInListings'))

    def update(self):
        self.actions = action.Actions(self, self.request, self.context)

        subform = GeopointContainerForm(self.context,  self.request, self)
        subform.update()
        subform.level = self.level + 1

        self.subforms = [subform, ]
        super(GeoContainerSettingsForm, self).update()

    @property
    def css_class(self):
        return "subform openlayers-level-%s" % self.level

    @property
    def parent_form(self):
        return self

    @property
    def next_url(self):
        #Need to send the user to the view url for certain content types.
        url = self.context.absolute_url()
        if self.context.portal_type in self.typesUseViewActionInListings:
            url += '/view'

        return url

    def redirectAction(self):
        self.request.response.redirect(self.next_url)

    def setStatusMessage(self, message):
        ptool = getToolByName(self.context,'plone_utils')
        ptool.addPortalMessage(message)

    @button.buttonAndHandler(_(u'Save'))
    def handleApply(self, action):
        subdata,  suberrors = self.subforms[0].extractData()
        data, errors = self.extractData()
        if errors or suberrors:
            return

        self.containersettings.initialiseSettings(self.context)

        for key, val in data.items():
            self.containersettings.set(key, val)

        for key, val in subdata.items():
            self.containersettings.set(key, val)

        notify(GeoContainerSettingsModifiedEvent(self.context))

        self.setStatusMessage(self.message_ok)
        self.redirectAction()

    @button.buttonAndHandler(_(u'Cancel'))
    def handleCancel(self, action):
        self.setStatusMessage(self.message_cancel)
        self.redirectAction()

    def updateWidgets(self):
        super(GeoContainerSettingsForm, self).updateWidgets()

    def getContent(self):
        '''See interfaces.IForm'''
        return self.containersettings.getSettings(self.context)

geoContainerSettings = wrap_form(GeoContainerSettingsForm, 
         label=_(u'Container-Specific Geo Settings'),
         description=_(u"Modify geo settings for the current container or Collection.")
)

