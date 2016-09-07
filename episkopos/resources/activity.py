# -*- coding: utf-8 -*-

"""
Created on 2016-08-19
:author: Izhar Firdaus (kagesenshi.87@gmail.com)
"""

from kotti.interfaces import IDefaultWorkflow
from kotti.resources import Content
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import Unicode
from sqlalchemy import LargeBinary
from sqlalchemy import DateTime
from sqlalchemy import Boolean
from sqlalchemy import UnicodeText
from sqlalchemy.orm import relationship
from zope.interface import implements
from depot.fields.sqlalchemy import UploadedFileField
from episkopos import _
from uuid import uuid4

class Activity(Content):
    __tablename__ = 'activities'

    implements(IDefaultWorkflow)

    id = Column(Integer, ForeignKey('contents.id'), primary_key=True)
    engagement_id = Column(Integer, ForeignKey('engagements.id'))
    engagement = relationship('Engagement',
                primaryjoin='Activity.engagement_id==Engagement.id')
    start_dt = Column(DateTime(timezone=True))
    end_dt = Column(DateTime(timezone=True))
    summary = Column(UnicodeText())
    issues = Column(UnicodeText())
    in_navigation = Column(Boolean, default=False)
    uuid = Column(Unicode(50))
    type_info = Content.type_info.copy(
        name=u'Activity',
        title=_(u'Activity'),
        add_view=u'add_activity',
        addable_to=[u'Document'],
        add_permission='episkopos.add_activity',
        selectable_default_views=[
#            ("alternative-view", _(u"Alternative view")),
        ],
    )

    def __init__(self,  engagement_id=None, start_dt=None, end_dt=None, 
                uuid=None, issues=None, **kwargs):
        """ Constructor

        :param custom_attribute: A very custom attribute
        :type custom_attribute: unicode

        :param **kwargs: Arguments that are passed to the base class(es)
        :type **kwargs: see :class:`kotti.resources.Content`
        """

        super(Activity, self).__init__(**kwargs)
        self.uuid = uuid or str(uuid4())
        self.engagement_id = engagement_id
        self.start_dt = start_dt
        self.end_dt = end_dt
        self.issues = issues

    @property
    def in_navigation(self):
        return False

    @in_navigation.setter
    def in_navigation(self, value):
        pass

