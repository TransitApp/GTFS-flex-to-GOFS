from dataclasses import dataclass
from gtfs_loader import schema
from typing import List

from ..gofs_file import GofsFile
from datetime import datetime, timedelta

FILENAME = 'calendars'

DAYS_OF_WEEK = {
    'monday': 'mon',
    'tuesday': 'tue',
    'wednesday': 'wed',
    'thursday': 'thu',
    'friday': 'fri',
    'saturday': 'sat',
    'sunday': 'sun'
}

@dataclass
class Calendar:
    calendar_id: str
    start_date: str
    end_date: str
    days: List[str]
    excepted_dates: List[str]


def create(gtfs, used_calendar_ids):
    used_calendar_ids = used_calendar_ids.copy() # Make a copy to avoid modifying the original list
    calendars = extract_calendar(gtfs, used_calendar_ids)
    calendars.extend(extract_calendar_dates_only_calendar(gtfs, used_calendar_ids))

    return GofsFile(FILENAME, created=True, data=calendars)

def extract_calendar(gtfs, used_calendar_ids):
    calendars = []
    for calendar in gtfs.calendar.values():
        if calendar.service_id not in used_calendar_ids:
            continue  # Only extract calender that are actually used by on demand services

        days = extract_service_days(calendar)

        excepted_dates = []
        if calendar.service_id in gtfs.calendar_dates:
            for calendar_date in gtfs.calendar_dates[calendar.service_id]:
                if calendar_date.exception_type is schema.ExceptionType.REMOVE:
                    excepted_dates.append(repr(calendar_date.date))

                if calendar_date.exception_type is schema.ExceptionType.ADD:
                    raise ValueError(f"Added dates are not supported, we need to support it in GOFS-lite first: {calendar.service_id}")

        calendar_data = Calendar(calendar.service_id, repr(
            calendar.start_date), repr(calendar.end_date), days, excepted_dates)
        used_calendar_ids.remove(calendar.service_id)

        calendars.append(calendar_data)
    return calendars

def extract_calendar_dates_only_calendar(gtfs, used_calendar_ids):
    calendars = []
    for calendar_id in used_calendar_ids:
        # Remaining calendar ids should be from calendar_dates, otherwise they are just missing
        if calendar_id in gtfs.calendar_dates:
            active_dates_calendar = []
            for calendar_date in gtfs.calendar_dates[calendar_id]:
                if calendar_date.exception_type is schema.ExceptionType.ADD:
                    if repr(calendar_date.date) not in active_dates_calendar:
                        active_dates_calendar.append(repr(calendar_date.date))
                elif calendar_date.exception_type is schema.ExceptionType.REMOVE:
                    if repr(calendar_date.date) in active_dates_calendar:
                        active_dates_calendar.remove(repr(calendar_date.date))

            # there's no support for a list of supported dates in GOFS-lite
            # instead, create a calendar from the start to the end date, then remove all the dates that are not in the active dates
            active_dates_calendar.sort()
            start_date = active_dates_calendar[0]
            end_date = active_dates_calendar[-1]

            start_date_dt = datetime.strptime(start_date, '%Y%m%d')
            end_date_dt = datetime.strptime(end_date, '%Y%m%d')

            all_dates = set()
            current_date = start_date_dt
            while current_date <= end_date_dt:
                all_dates.add(current_date.strftime('%Y%m%d'))
                current_date += timedelta(days=1)

            active_dates_set = set(active_dates_calendar)
            missing_dates = all_dates - active_dates_set

            excepted_dates = sorted(list(missing_dates))

            days = list(DAYS_OF_WEEK.values())
            calendar_data = Calendar(calendar_id, start_date, end_date, days, excepted_dates)
            calendars.append(calendar_data)
    return calendars

def extract_service_days(calendar):
    days = []
    for day_attr, day_str in DAYS_OF_WEEK.items():
        if getattr(calendar, day_attr):
            days.append(day_str)
    return days
