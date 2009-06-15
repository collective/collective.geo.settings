from z3c.form import field,  form, subform, button
from plone.z3cform import z2

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
    fields = field.Fields(IGeoSettings).select('latitude', 'longitude')

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
        subform.update()
        subform.level = self.level + 1

        self.subforms = [subform, ]

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

    def contents(self):
        z2.switch_on(self)
        form = GeoControlpanelForm(self.context, self.request)
        form.update()
        return form.render()

