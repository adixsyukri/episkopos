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
from sqlalchemy.orm import relationship
from zope.interface import implements
from depot.fields.sqlalchemy import UploadedFileField
from episkopos import _
from uuid import uuid4

class Engagement(Content):
    """ A company content type. """
    __versioned__ = {}
    __tablename__ = 'engagements'

    implements(IDefaultWorkflow)

    id = Column(Integer, ForeignKey('contents.id'), primary_key=True)
    engagement_code = Column(Unicode(1000))
    customer_id = Column(Integer, ForeignKey('companies.id'))
    customer = relationship('Company',
                primaryjoin='Engagement.customer_id==Company.id')

    uuid = Column(Unicode(50))
    type_info = Content.type_info.copy(
        name=u'Engagement',
        title=_(u'Engagement'),
        add_view=u'add_engagement',
        addable_to=[u'Document'],
        add_permission='episkopos.add_engagement',
        selectable_default_views=[
#            ("alternative-view", _(u"Alternative view")),
        ],
    )

    def __init__(self,  engagement_code=None, customer_id=None, uuid=None, **kwargs):
        """ Constructor

        :param custom_attribute: A very custom attribute
        :type custom_attribute: unicode

        :param **kwargs: Arguments that are passed to the base class(es)
        :type **kwargs: see :class:`kotti.resources.Content`
        """

        super(Engagement, self).__init__(**kwargs)

        self.engagement_code = engagement_code
        self.customer_id = customer_id
        self.uuid = uuid or str(uuid4())
        
    @property
    def in_navigation(self):
        return False

    @in_navigation.setter
    def in_navigation(self, value):
        pass

