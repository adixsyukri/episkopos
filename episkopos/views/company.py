# -*- coding: utf-8 -*-

"""
Created on 2016-08-19
:author: Izhar Firdaus (kagesenshi.87@gmail.com)
"""

import colander
from kotti.views.edit import ContentSchema
from kotti.views.form import AddFormView
from kotti.views.form import EditFormView
from deform import FileData
from deform.widget import FileUploadWidget

from pyramid.view import view_config
from pyramid.view import view_defaults
from pyramid.httpexceptions import HTTPFound

from episkopos import _
from episkopos.resources import Company

from episkopos.fanstatic import css_and_js
from episkopos.views import BaseView
from kotti.views.form import FileUploadTempStore
from kotti.views.form import get_appstruct
from kotti.views.form import validate_file_size_limit
from kotti.resources import get_root
from kotti.util import _to_fieldstorage

from StringIO import StringIO
import random
from uuid import uuid4

def CompanySchema(tmpstore):
    class CompanySchema(ContentSchema):
        """ Schema for CustomContent. """

        registration_number = colander.SchemaNode(
            colander.String(),
            title=_(u"Registration Number"))

#        logo = colander.SchemaNode(
#            FileData(),
#            title=_(u'Logo'),
#            widget=FileUploadWidget(tmpstore),
#            validator=validate_file_size_limit,
#        )
    return CompanySchema()
    

@view_config(name=Company.type_info.add_view, 
             permission=Company.type_info.add_permission,
             renderer='kotti:templates/edit/node.pt')
class CompanyAddForm(AddFormView):
    """ Form to add a new instance of Company. """
    item_type = _(u"Company")

    def schema_factory(self):
        tmpstore = FileUploadTempStore(self.request)
        return CompanySchema(tmpstore)

    def find_name(self, appstruct):
        appstruct.setdefault('uuid', str(uuid4()))
        return appstruct['uuid']

    def save_success(self, appstruct):
        result = super(CompanyAddForm, self).save_success(appstruct)
        name = appstruct['uuid']
        new_item = get_root()[name] = self.context[name]
        location = self.success_url or self.request.resource_url(new_item)
        return HTTPFound(location=location)

    def add(self, **appstruct):
#        appstruct['logo'] = _to_fieldstorage(**appstruct['logo'])
        return Company(**appstruct)


@view_config(name='edit', context=Company, permission='edit',
             renderer='kotti:templates/edit/node.pt')
class CompanyEditForm(EditFormView):
    """ Form to edit existing Company objects. """

    def schema_factory(self):
        tmpstore = FileUploadTempStore(self.request)
        return CompanySchema(tmpstore)

#    def before(self, form):
#        form.appstruct = get_appstruct(self.context, self.schema)
#        if self.context.logo is not None:
#            form.appstruct['logo'] = {
#                'uid': str(random.randint(1000000000, 9999999999)),
#                'filename' : form.appstruct['logo']['filename'],
#                'mimetype': form.appstruct['logo']['content_type'],
#                'fp': StringIO(self.context.logo.file.read())
#            }
#
    def edit(self, **appstruct):
#        appstruct['logo'] = _to_fieldstorage(**appstruct['logo'])
        return super(CompanyEditForm, self).edit(**appstruct)


@view_defaults(context=Company, permission='view')
class CompanyViews(BaseView):
    """ Views for :class:`episkopos.resources.Company` """

    @view_config(name='view', permission='view',
                 renderer='episkopos:templates/company.pt')
    def default_view(self):
        """ Default view for :class:`episkopos.resources.Company`

        :result: Dictionary needed to render the template.
        :rtype: dict
        """

        return {
            'foo': _(u'bar'),
        }
