from z3c.form import field,  form, subform, button
from z3c.form.interfaces import IFormLayer
from plone.z3cform import z2

from Acquisition import aq_inner

from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from zope.component import getUtility
from zope.app.pagetemplate import viewpagetemplatefile
from zope.app.component.hooks import getSite

from collective.geo.geopoint.geopointform import GeopointBaseForm
from collective.geo.settings.interfaces import IGeoSettings
from collective.geo.settings import GeoSettingsMessageFactory as _

def geo_settings(context):
    return getUtility(IGeoSettings)

def back_to_controlpanel(self):
    root = getSite()
    return dict(url=root.absolute_url() + '/plone_control_panel')

class GeopointForm(GeopointBaseForm, subform.EditSubForm):
    fields = field.Fields(IGeoSettings).select('longitude', 'latitude')

    def update(self):
        self.updateWidgets()



class GeoControlpanelForm(form.EditForm):
    template = viewpagetemplatefile.ViewPageTemplateFile('form-with-subforms.pt')

    fields = field.Fields(IGeoSettings).select('zoom', 'googlemaps', 'googleapi')

    heading = _(u'Configure Collective Geo Settings')

    @property
    def css_class(self):
        return "subform openlayers-level-%s" % self.level

    level = 1

    def __init__(self, context, request):
        super(GeoControlpanelForm,self).__init__(context,request)

        subform = GeopointForm(self.context,  self.request, self)
        subform.level = self.level + 1

        self.subforms = [subform, ]

    def update(self):
        # updatu subforms first, else the values won't be available in button handler
        for subform in self.subforms:
            subform.update()
        super(GeoControlpanelForm, self).update()

    def updateWidgets(self):
        super(GeoControlpanelForm, self).updateWidgets()
        self.widgets['googleapi'].size = 80

    @property
    def parent_form(self):
        return self

    @button.handler(form.EditForm.buttons['apply'])
    def handle_add(self, action):
        subdata,  suberrors = self.subforms[0].extractData()
        data, errors = self.extractData()
        if errors or suberrors:
            return

        utility = IGeoSettings(self.context)
        for key, val in data.items():
            utility.set(key, val)

        for key, val in subdata.items():
            utility.set(key, val)

class GeoControlpanel(BrowserView):

    __call__ = ViewPageTemplateFile('controlpanel.pt')

    label = _(u'Geo Settings')
    description = _(u"Collective Geo Default Settings")
    back_link = back_to_controlpanel

    request_layer = IFormLayer
    form = GeoControlpanelForm

    # NOTE: init code taken from plone.z3cform FormWrapper...
    #       maybe extending FormWrapper would be an option?
    def __init__(self, context, request):
        super(GeoControlpanel, self).__init__(context, request)
        if self.form is not None:
            self.form_instance = self.form(aq_inner(self.context), self.request)
            self.form_instance.__name__ = self.__name__

    def contents(self):
        z2.switch_on(self)
        self.form_instance.update()
        return self.form_instance.render()
