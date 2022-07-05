from copy import deepcopy
from gtfs_loader.schema import BookingType

from .save_file import *
from .utils import GofsFile

FILENAME = 'wait_times.json'

MINUTE = 60
HOUR = 60 * MINUTE
DAY = 24 * HOUR

def convert_to_wait_time(booking_rule):
    if booking_rule is None:
        return -1

    if booking_rule.booking_type == BookingType.REAL_TIME:
        return 0

    if booking_rule.booking_type == BookingType.SAME_DAY:
        return booking_rule.prior_notice_duration_min * MINUTE

    if booking_rule.booking_type == BookingType.UP_TO_PRIOR_DAYS:
        return booking_rule.prior_notice_last_day * DAY


def create_wait_times_file(gtfs, gofs_dir, default_headers_template, pickup_booking_rule_ids):
    file = deepcopy(default_headers_template)

    wait_times = []
    for pickup_booking_rule_id, transfers in pickup_booking_rule_ids.items():
        for transfer in transfers:
            wait_time = convert_to_wait_time(
                gtfs.booking_rules[pickup_booking_rule_id])
            wait_times.append({
                'zone_ids': [transfer.from_stop_id],
                'to_zone_ids': [transfer.to_stop_id],
                'wait_time': wait_time
            })

    file['data']['wait_times'] = wait_times

    save_file(gofs_dir / FILENAME, file)
    return GofsFile(FILENAME, True)
