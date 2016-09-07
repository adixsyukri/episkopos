from sqlalchemy.types import TypeDecorator, DateTime
from dateutil.tz import tzutc
from pytz import timezone
from datetime import datetime

class UTCDateTime(TypeDecorator):

    impl = DateTime

    def process_bind_param(self, value, engine):
        if value is not None:
            return value.astimezone(tzutc()).replace(tzinfo=None)

    def process_result_value(self, value, engine):
        if value is not None:
            return value.replace(
                tzinfo=tzutc()).astimezone(timezone('Asia/Kuala_Lumpur'))

