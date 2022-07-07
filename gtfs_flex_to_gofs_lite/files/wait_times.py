from dataclasses import dataclass
from gtfs_loader.schema import BookingType
from typing import List

from ..gofs_file import GofsFile

FILENAME = 'wait_times'

MINUTE = 60
HOUR = 60 * MINUTE
DAY = 24 * HOUR


@dataclass
class WaitTimes:
    zone_ids: List[str]
    to_zone_ids: List[str]
    wait_time: int


def create(gtfs, pickup_booking_rule_ids):
    wait_times = []
    for pickup_booking_rule_id, transfers in pickup_booking_rule_ids.items():
        for transfer in transfers:
            wait_time = convert_to_wait_time(
                gtfs.booking_rules[pickup_booking_rule_id])
            wait_times.append(WaitTimes(
                zone_ids=[transfer.from_stop_id],
                to_zone_ids=[transfer.to_stop_id],  # Not part of specs yet
                wait_time=wait_time
            ))

    return GofsFile(FILENAME, created=True, data=wait_times)


def convert_to_wait_time(booking_rule):
    if booking_rule is None:
        return -1

    if booking_rule.booking_type == BookingType.REAL_TIME:
        return 0

    if booking_rule.booking_type == BookingType.SAME_DAY:
        return booking_rule.prior_notice_duration_min * MINUTE

    if booking_rule.booking_type == BookingType.UP_TO_PRIOR_DAYS:
        return booking_rule.prior_notice_last_day * DAY
