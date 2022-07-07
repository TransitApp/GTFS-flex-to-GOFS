from dataclasses import dataclass
from gtfs_loader import schema
from typing import List

from ..gofs_file import GofsFile

FILENAME = 'calendars'


@dataclass
class Calendar:
    calendar_id: str
    start_date: str
    end_date: str
    days: List[str]
    excepted_dates: List[str]


def create(gtfs, used_calendar_ids):
    calendars_data = []
    for calendar in gtfs.calendar.values():
        if not calendar.service_id in used_calendar_ids:
            continue  # Only extract calender that are actually used by on demand services

        days = []
        if calendar.monday:
            days.append('mon')
        if calendar.tuesday:
            days.append('tue')
        if calendar.wednesday:
            days.append('wed')
        if calendar.thursday:
            days.append('thu')
        if calendar.friday:
            days.append('fri')
        if calendar.saturday:
            days.append('sat')
        if calendar.sunday:
            days.append('sun')

        excepted_dates = []
        if calendar.service_id in gtfs.calendar_dates:
            for calendar_date in gtfs.calendar_dates[calendar.service_id]:
                if calendar_date.exception_type is schema.ExceptionType.REMOVE:
                    excepted_dates.append(repr(calendar_date.date))
                
                if calendar_date.exception_type is schema.ExceptionType.ADD:
                    # TODO
                    pass

        calendar_data = Calendar(calendar.service_id, repr(
            calendar.start_date), repr(calendar.end_date), days, excepted_dates)

        calendars_data.append(calendar_data)

    return GofsFile(FILENAME, created=True, data=calendars_data)
