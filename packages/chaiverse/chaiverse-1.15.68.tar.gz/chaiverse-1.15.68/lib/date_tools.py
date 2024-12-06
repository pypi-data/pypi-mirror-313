from datetime import datetime, timezone
import dateparser
import pytz
from typing import Optional

from typing_extensions import Literal

from chaiverse.schemas.date_range_schema import DateRange

US_PACIFIC = pytz.timezone('US/Pacific')
UTC = pytz.timezone('UTC')


def is_epoch_time_before_date_range(epoch_time, date_range: Optional[DateRange]):
    is_before = date_range and epoch_time < date_range.start_epoch_time
    return is_before


def is_epoch_time_in_date_range(epoch_time, date_range: Optional[DateRange]):
    is_in = True
    if date_range:
        is_in = date_range.start_epoch_time <= epoch_time < date_range.end_epoch_time
    return is_in


def us_pacific_date_string() -> str:
    date = datetime.now(US_PACIFIC)
    date_string = date.strftime('%Y-%m-%d')
    return date_string


def us_pacific_string(date_string: Optional[str]=None):
    return _create_date_string_in_timezone(US_PACIFIC, date_string)


def utc_string(date_string: Optional[str]=None):
    return _create_date_string_in_timezone(UTC, date_string)


def convert_to_utc_iso_format(date_string: Optional[str], default_timezone=US_PACIFIC):
    date_string_in_utc = None
    if date_string is not None:
        date = datetime.fromisoformat(date_string)
        date = default_timezone.localize(date) if not date.tzinfo else date
        date_in_utc = date.astimezone(timezone.utc)
        date_string_in_utc = date_in_utc.isoformat()
    return date_string_in_utc


def convert_to_us_pacific_date(date: Optional[datetime], default_timezone=UTC):
    date_in_us_pacific = None
    if date is not None:
        date = default_timezone.localize(date) if not date.tzinfo else date
        date_in_us_pacific = date.astimezone(US_PACIFIC)
    return date_in_us_pacific


def _create_date_string_in_timezone(pytz_timezone, date_string: Optional[str]=None):
    if date_string:
        date = dateparser.parse(date_string)
        date = pytz_timezone.localize(date)
    else:
        date = datetime.now(pytz_timezone)
    return date.isoformat()


def _get_date_range_field(date_range=None, field=Literal['start_date', 'end_date']):
    epoch_time = None
    if date_range and date_range.get(field):
        isoformat_date = date_range.get(field)
        date = datetime.fromisoformat(isoformat_date) 
        assert date.tzinfo
        epoch_time = date.timestamp()
    return epoch_time
