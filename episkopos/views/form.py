import colander
from deform import widget
from episkopos.resources import Engagement
from episkopos.resources import Company
from uuid import uuid4
from pytz import timezone
from datetime import datetime

@colander.deferred
def deferred_company_select_widget(node, kw):
    values = [(i.id, i.title) for i in Company.query.all()]
    return widget.SelectWidget(values=values)

@colander.deferred
def deferred_engagement_select_widget(node, kw):
    values = [(i.id, i.title) for i in Engagement.query.all()]
    return widget.SelectWidget(values=values)

@colander.deferred
def deferred_default_uuid(node, kw):
    return str(uuid4())

@colander.deferred
def deferred_default_dt(node, kw):
    now = datetime.now(timezone('Asia/Kuala_Lumpur'))
    return datetime(now.year, now.month, now.day, now.hour, 0,
            tzinfo=now.tzinfo)
