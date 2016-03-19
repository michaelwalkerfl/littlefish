"""
This contains functions to manipulate and display timestamps
"""

__author__ = 'Stephen Brown (Little Fish Solutions LTD)'

import logging
import datetime
import calendar

import pytz

log = logging.getLogger(__name__)

utc = pytz.utc
local = pytz.timezone('Europe/London')


def to_local_time(time_in):
    if not hasattr(time_in, 'tzinfo'):
        # This is a date with no timestamp info so we can't do the conversion
        return time_in
    elif time_in.tzinfo is None:
        # If there is no timezone, localise it to UTC
        time_utc = utc.localize(time_in)
    elif time_in.tzinfo.zone == 'UTC':
        # Already UTC - no need to localize
        time_utc = time_in
    else:
        # Not a UTC timestamp
        raise Exception('Not a UTC time: %s' % time_in)
    
    time_local = time_utc.astimezone(local)
    # Strip off timezone info
    return time_local.replace(tzinfo=None)


def to_utc_time(time_in):
    if not hasattr(time_in, 'tzinfo'):
        # This is a date with no timestamp info so we can't do the conversion
        return time_in
    elif time_in.tzinfo is None:
        # If there is no timezone, localise it to local time
        time_local = local.localize(time_in)
    elif time_in.tzinfo.zone == local.zone:
        # Already local - no need to localize
        time_local = time_in
    else:
        # Not a local timestamp
        raise Exception('Not a local time: %s' % time_in)

    time_utc = time_local.astimezone(utc)
    # Strip off timezone info
    return time_utc.replace(tzinfo=None)


def format_datetime(datetime, convert_to_local=True):
    if datetime:
        if convert_to_local:
            local_datetime = to_local_time(datetime)
            return local_datetime.strftime('%d/%m/%Y %H:%M:%S')
        else:
            return datetime.strftime('%d/%m/%Y %H:%M:%S')
    else:
        return ''


def format_datetime_long(datetime, convert_to_local=True):
    if datetime:
        if convert_to_local:
            local_datetime = to_local_time(datetime)
            return local_datetime.strftime('%A %d %B %Y %H:%M:%S')
        else:
            return datetime.strftime('%A %d %B %Y %H:%M:%S')
    else:
        return ''


def format_date(datetime, convert_to_local=True):
    if datetime:
        try:
            if convert_to_local:
                local_datetime = to_local_time(datetime)
                return local_datetime.strftime('%d/%m/%Y')
            else:
                return datetime.strftime('%d/%m/%Y')
        except ValueError:
            log.warning('Invalid date: %s' % datetime)
            return '????'
    else:
        return ''


def format_date_long(datetime, convert_to_local=True):
    if datetime:
        try:
            if convert_to_local:
                local_datetime = to_local_time(datetime)
                return local_datetime.strftime('%A %d %B %Y')
            else:
                return datetime.strftime('%A %d %B %Y')
        except ValueError:
            log.warning('Invalid date: %s' % datetime)
            return '????'
    else:
        return ''


def format_date_long_no_day(datetime, convert_to_local=True):
    if datetime:
        try:
            if convert_to_local:
                local_datetime = to_local_time(datetime)
                return local_datetime.strftime('%d %B %Y')
            else:
                return datetime.strftime('%d %B %Y')
        except ValueError:
            log.warning('Invalid date: %s' % datetime)
            return '????'
    else:
        return ''


def add_working_days(num_days, date=None, include_saturday=False):
    if date is None:
        date = datetime.date.today()
        
    for i in range(num_days):
        date += datetime.timedelta(days=1)
        while date.weekday() == 6 or (not include_saturday and date.weekday() == 5):
            date += datetime.timedelta(days=1)
        
    return date


def datetime_from_datepicker(date_string):
    """Turn a string from a jQuery UI datetpicker into a datetime object"""
    return datetime.datetime.strptime(date_string, '%d/%m/%Y')


def date_from_datepicker(date_string):
    """Turn a string from a jQuery UI datetpicker into a datetime object"""
    return datetime_from_datepicker(date_string).date()


def datetime_to_datepicker(timestamp):
    """Turn a datetime object back into a string for a JQuery UI datepicker"""
    return timestamp.strftime('%d/%m/%Y')


def add_months(months, timestamp=datetime.datetime.utcnow()):
    """Add a number of months to a timestamp"""
    month = timestamp.month
    new_month = month + months
    years = 0
    
    while new_month < 1:
        new_month += 12
        years -= 1
    
    while new_month > 12:
        new_month -= 12
        years += 1
    
    # month = timestamp.month
    year = timestamp.year + years

    try:
        return datetime.datetime(year, new_month, timestamp.day, timestamp.hour, timestamp.minute, timestamp.second)
    except ValueError:
        # This means that the day exceeds the last day of the month, i.e. it is 30th March, and we are finding the day
        # 1 month ago, and it is trying to return 30th February
        if months > 0:
            # We are adding, so use the first day of the next month
            new_month += 1
            if new_month > 12:
                new_month -= 12
                year += 1
            
            return datetime.datetime(year, new_month, 1, timestamp.hour, timestamp.minute, timestamp.second)
        else:
            # We are subtracting - use the last day of the same month
            new_day = calendar.monthrange(year, new_month)[1]
            return datetime.datetime(year, new_month, new_day, timestamp.hour, timestamp.minute, timestamp.second)


def add_months_to_date(months, date):
    """Add a number of months to a date"""
    month = date.month
    new_month = month + months
    years = 0

    while new_month < 1:
        new_month += 12
        years -= 1

    while new_month > 12:
        new_month -= 12
        years += 1

    # month = timestamp.month
    year = date.year + years

    try:
        return datetime.date(year, new_month, date.day)
    except ValueError:
        # This means that the day exceeds the last day of the month, i.e. it is 30th March, and we are finding the day
        # 1 month ago, and it is trying to return 30th February
        if months > 0:
            # We are adding, so use the first day of the next month
            new_month += 1
            if new_month > 12:
                new_month -= 12
                year += 1

            return datetime.datetime(year, new_month, 1)
        else:
            # We are subtracting - use the last day of the same month
            new_day = calendar.monthrange(year, new_month)[1]
            return datetime.datetime(year, new_month, new_day)


def unix_time(dt=None):
    """Generate a unix style timestamp (in seconds)"""
    if dt is None:
        dt = datetime.datetime.utcnow()

    epoch = datetime.datetime.utcfromtimestamp(0)
    delta = dt - epoch
    return delta.total_seconds()
