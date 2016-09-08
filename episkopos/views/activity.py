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
from pyramid.httpexceptions import HTTPFound

from episkopos import _
from episkopos.resources import Activity

from episkopos.fanstatic import css_and_js
from episkopos.views import BaseView
from episkopos.views.form import deferred_default_uuid
from episkopos.views.form import deferred_default_dt

from kotti.resources import get_root
from kotti.views.form import FileUploadTempStore
from kotti.views.form import get_appstruct
from kotti.views.form import validate_file_size_limit
from kotti.util import _to_fieldstorage

from episkopos.views.form import deferred_engagement_select_widget 

from pytz import timezone
from StringIO import StringIO
from iso8601.iso8601 import FixedOffset
import random
from uuid import uuid4
from kotti import DBSession
from deform.widget import RichTextWidget
from sqlalchemy import desc

def ActivitySchema(tmpstore):
    class ActivitySchema(colander.MappingSchema):
        """ Schema for CustomContent. """

        engagement_id = colander.SchemaNode(
            colander.Integer(),
            title=_(u"Engagement"),
            widget=deferred_engagement_select_widget)

        start_dt = colander.SchemaNode(
            colander.DateTime(default_tzinfo=FixedOffset(8, 0, 'Asia/Kuala_Lumpur')),
            title=_(u'Start'),
            widget=DateTimeInputWidget(
                time_options=(('format', 'h:i A'), ('interval', 60))
            ),
            default=deferred_default_dt
        )
        end_dt = colander.SchemaNode(
            colander.DateTime(default_tzinfo=FixedOffset(8, 0, 'Asia/Kuala_Lumpur')),
            title=_(u'End'),
            widget=DateTimeInputWidget(
                time_options=(('format', 'h:i A'), ('interval', 60))
            ),
            default=deferred_default_dt
        )

        summary = colander.SchemaNode(
            colander.String(),
            title=_('Activity Summary'),
            widget=RichTextWidget(),
            missing=u"",
        )

        issues = colander.SchemaNode(
            colander.String(),
            title=_('Issues Faced'),
            widget=RichTextWidget(),
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
        appstruct.setdefault('uuid', str(uuid4()))
        return appstruct['uuid']

    def save_success(self, appstruct):
        appstruct['start_dt'] = appstruct['start_dt'].replace(minute=0)
        appstruct['end_dt'] = appstruct['end_dt'].replace(minute=0)
        result = super(ActivityAddForm, self).save_success(appstruct)
        name = appstruct['uuid']
        new_item = get_root()[name] = self.context[name]
        location = self.request.application_url + '/activities'
        return HTTPFound(location=location)


@view_config(name='edit', context=Activity, permission='edit',
             renderer='kotti:templates/edit/node.pt')
class ActivityEditForm(EditFormView):
    """ Form to edit existing Activity objects. """

    def schema_factory(self):
        tmpstore = FileUploadTempStore(self.request)
        return ActivitySchema(tmpstore)

    def edit(self, **appstruct):
        appstruct['start_dt'] = appstruct['start_dt'].replace(minute=0)
        appstruct['end_dt'] = appstruct['end_dt'].replace(minute=0)
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


class GlobalViews(BaseView):
    @view_config(name='activities', permission='view',
            renderer='episkopos:templates/table.pt')
    def activities(self):
        def get_date(d):
            return d.strftime('%Y-%m-%d %H:%M') if d else ''
            
        return {
                'headers': [
                        {'key': 'owner', 
                         'label': _(u'Owner'), 
                         'structure': False},
                        {'key': 'start_dt', 
                         'label': _(u'Start Date'), 
                         'structure': False},
                        {'key': 'end_dt', 
                         'label': _(u'End Date'), 
                         'structure': False},
                        {'key': 'summary', 
                         'label': _(u'Summary'), 
                         'structure': True},
                        {'key': 'issues', 
                         'label': _(u'Issues'), 
                         'structure': True},
                        {'key': 'engagement', 
                         'label': _(u'Engagement'), 
                         'structure': False}],
            'data': [{
                'url': self.request.resource_url(i),
                'start_dt': get_date(i.start_dt),
                'end_dt': get_date(i.end_dt),
                'owner': i.owner,
                'summary': i.summary,
                'issues': i.issues,
                'engagement': i.engagement.title
            } for i in DBSession.query(
                Activity).order_by(desc(Activity.creation_date)
                ).limit(15).all()]}
