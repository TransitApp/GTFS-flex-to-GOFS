from copy import deepcopy
from gtfs_loader import schema

from .default_headers import get_default_headers
from .utils import GofsFile
from .save_file import *

FILENAME = 'calendar.json'

def create_calendar_file(gtfs, gofs_dir, default_headers_template, used_calendar_ids):
    file = deepcopy(default_headers_template)

    calendars = []

    for calendar in gtfs.calendar.values():
        if not calendar.service_id in used_calendar_ids:
            continue  # Only extract calender that are actually used by on demand services

        gofs_calendar = {
            'calendar_id': calendar.service_id,
            'start_date': repr(calendar.start_date),
            'end_date': repr(calendar.end_date)
        }

        gofs_calendar['days'] = []
        if calendar.monday:
            gofs_calendar['days'].append('mon')
        if calendar.tuesday:
            gofs_calendar['days'].append('tue')
        if calendar.wednesday:
            gofs_calendar['days'].append('wed')
        if calendar.thursday:
            gofs_calendar['days'].append('thu')
        if calendar.friday:
            gofs_calendar['days'].append('fri')
        if calendar.saturday:
            gofs_calendar['days'].append('sat')
        if calendar.sunday:
            gofs_calendar['days'].append('sun')

        gofs_calendar['excepted_dates'] = []
        if calendar.service_id in gtfs.calendar_dates:
            for calendar_date in gtfs.calendar_dates[calendar.service_id]:
                if calendar_date.exception_type is not schema.ExceptionType.REMOVE:
                    continue

                gofs_calendar['excepted_dates'].append(
                    repr(calendar_date.date))

        calendars.append(gofs_calendar)

    file['data']['calendars'] = calendars

    save_file(gofs_dir / FILENAME, file)
    return GofsFile(FILENAME, True)
