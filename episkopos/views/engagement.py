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
from episkopos.resources import Engagement

from episkopos.fanstatic import css_and_js
from episkopos.views import BaseView
from kotti.views.form import FileUploadTempStore
from kotti.views.form import get_appstruct
from kotti.views.form import validate_file_size_limit
from kotti.resources import get_root
from kotti.util import _to_fieldstorage
from episkopos.views.form import deferred_company_select_widget

from StringIO import StringIO
import random
from uuid import uuid4

def EngagementSchema(tmpstore):
    class EngagementSchema(ContentSchema):
        """ Schema for CustomContent. """

        engagement_code = colander.SchemaNode(
            colander.String(),
            title=_(u"Engagement Code"))

        customer_id = colander.SchemaNode(
            colander.Integer(),
            title=_(u'Customer'),
            widget=deferred_company_select_widget
        )
    return EngagementSchema()
    

@view_config(name=Engagement.type_info.add_view, 
             permission=Engagement.type_info.add_permission,
             renderer='kotti:templates/edit/node.pt')
class EngagementAddForm(AddFormView):
    """ Form to add a new instance of Engagement. """
    item_type = _(u"Engagement")

    def schema_factory(self):
        tmpstore = FileUploadTempStore(self.request)
        return EngagementSchema(tmpstore)

    def add(self, **appstruct):
        return Engagement(**appstruct)

    def find_name(self, appstruct):
        appstruct.setdefault('uuid', str(uuid4()))
        return appstruct['uuid']

    def save_success(self, appstruct):
        result = super(EngagementAddForm, self).save_success(appstruct)
        name = appstruct['uuid'] 
        new_item = get_root()[name] = self.context[name]
        location = self.success_url or self.request.resource_url(new_item)
        return HTTPFound(location=location)

@view_config(name='edit', context=Engagement, permission='edit',
             renderer='kotti:templates/edit/node.pt')
class EngagementEditForm(EditFormView):
    """ Form to edit existing Engagement objects. """

    def schema_factory(self):
        tmpstore = FileUploadTempStore(self.request)
        return EngagementSchema(tmpstore)

    def edit(self, **appstruct):
        return super(EngagementEditForm, self).edit(**appstruct)


@view_defaults(context=Engagement, permission='view')
class EngagementViews(BaseView):
    """ Views for :class:`episkopos.resources.Engagement` """

    @view_config(name='view', permission='view',
                 renderer='episkopos:templates/engagement.pt')
    def default_view(self):
        """ Default view for :class:`episkopos.resources.Engagement`

        :result: Dictionary needed to render the template.
        :rtype: dict
        """

        return {
            'foo': _(u'bar'),
        }
