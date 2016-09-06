# -*- coding: utf-8 -*-

"""
Created on 2016-08-19
:author: Izhar Firdaus (kagesenshi.87@gmail.com)
"""

import colander
from kotti.views.edit import ContentSchema
from kotti.views.form import AddFormView
from kotti.views.form import EditFormView
from kotti.views.form import deferred_tag_it_widget, ObjectType
from deform import FileData
from deform.widget import FileUploadWidget
from deform.widget import TextAreaWidget
from deform.widget import DateTimeInputWidget
from deform.widget import HiddenWidget

from pyramid.view import view_config
from pyramid.view import view_defaults

from episkopos import _
from episkopos.resources import Activity

from episkopos.fanstatic import css_and_js
from episkopos.views import BaseView
from episkopos.views.form import deferred_default_uuid
from episkopos.views.form import deferred_default_dt

from kotti.views.form import FileUploadTempStore
from kotti.views.form import get_appstruct
from kotti.views.form import validate_file_size_limit
from kotti.util import _to_fieldstorage

from episkopos.views.form import deferred_engagement_select_widget 

from pytz import timezone
from StringIO import StringIO
import random
from uuid import uuid4

def ActivitySchema(tmpstore):
    class ActivitySchema(colander.MappingSchema):
        """ Schema for CustomContent. """

        engagement_id = colander.SchemaNode(
            colander.Integer(),
            title=_(u"Engagement"),
            widget=deferred_engagement_select_widget)

        start_dt = colander.SchemaNode(
            colander.DateTime(default_tzinfo=timezone('Asia/Kuala_Lumpur')),
            title=_(u'Start'),
            widget=DateTimeInputWidget(
                time_options=(('format', 'h:i A'), ('interval', 60))
            ),
            default=deferred_default_dt
        )
        end_dt = colander.SchemaNode(
            colander.DateTime(default_tzinfo=timezone('Asia/Kuala_Lumpur')),
            title=_(u'End'),
            widget=DateTimeInputWidget(
                time_options=(('format', 'h:i A'), ('interval', 60))
            ),
            default=deferred_default_dt
        )

        description = colander.SchemaNode(
            colander.String(),
            title=_('Activity Summary'),
            widget=TextAreaWidget(cols=40, rows=5),
            missing=u"",
        )

        issues = colander.SchemaNode(
            colander.String(),
            title=_('Issues Faced'),
            widget=TextAreaWidget(cols=40, rows=5),
            missing=u"",
        )
    
        tags = colander.SchemaNode(
            ObjectType(),
            title=_('Tags'),
            widget=deferred_tag_it_widget,
            missing=[],
        )
    return ActivitySchema()
    

@view_config(name=Activity.type_info.add_view, 
             permission=Activity.type_info.add_permission,
             renderer='kotti:templates/edit/node.pt')
class ActivityAddForm(AddFormView):
    """ Form to add a new instance of Activity. """
    item_type = _(u"Activity")

    def schema_factory(self):
        tmpstore = FileUploadTempStore(self.request)
        return ActivitySchema(tmpstore)

    def add(self, **appstruct):
        title = '%s (%s to %s)' % (
            self.request.user.name,
            appstruct['start_dt'].strftime('%Y-%m-%d %H:%M'),
            appstruct['end_dt'].strftime('%Y-%m-%d %H:%M')
        )
        appstruct['title'] = title
        return Activity(**appstruct)

    def find_name(self, appstruct):
        uuid = str(uuid4())
        appstruct['uuid'] = uuid
        return uuid


@view_config(name='edit', context=Activity, permission='edit',
             renderer='kotti:templates/edit/node.pt')
class ActivityEditForm(EditFormView):
    """ Form to edit existing Activity objects. """

    def schema_factory(self):
        tmpstore = FileUploadTempStore(self.request)
        return ActivitySchema(tmpstore)

    def edit(self, **appstruct):
        return super(ActivityEditForm, self).edit(**appstruct)


@view_defaults(context=Activity, permission='view')
class ActivityViews(BaseView):
    """ Views for :class:`episkopos.resources.Activity` """

    @view_config(name='view', permission='view',
                 renderer='episkopos:templates/engagement.pt')
    def default_view(self):
        """ Default view for :class:`episkopos.resources.Activity`

        :result: Dictionary needed to render the template.
        :rtype: dict
        """

        return {
            'foo': _(u'bar'),
        }
