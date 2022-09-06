from dataclasses import dataclass
from gtfs_flex_to_gofs_lite.files import booking_rules
from gtfs_loader.schema import BookingType
from typing import List

from ..gofs_file import GofsFile

FILENAME = 'booking_rules'

MINUTE = 60
HOUR = 60 * MINUTE
DAY = 24 * HOUR


@dataclass
class BookingRules:
    from_zone_ids: List[str]
    to_zone_ids: List[str]
    booking_type: int
    prior_notice_duration_min: int
    prior_notice_duration_max: int
    prior_notice_last_day: int
    prior_notice_last_time: int
    prior_notice_last_time: int
    prior_notice_start_time: int
    prior_notice_calendar_id: int
    message: str
    pickup_message: str
    drop_off_message: str
    phone_number: str
    info_url: str
    booking_url: str


def create(gtfs, pickup_booking_rule_ids):
    booking_rules = []
    for pickup_booking_rule_id, transfers in pickup_booking_rule_ids.items():
        for transfer in transfers:
            gtfs_booking_rule = gtfs.booking_rules[pickup_booking_rule_id]

            booking_rules.append(BookingRules(
                from_zone_ids=[transfer.from_stop_id],
                to_zone_ids=[transfer.to_stop_id],
                booking_type=gtfs_booking_rule.booking_type,
                prior_notice_duration_min=gtfs_booking_rule.prior_notice_duration_min,
                prior_notice_duration_max=gtfs_booking_rule.prior_notice_duration_max,
                prior_notice_last_day=gtfs_booking_rule.prior_notice_last_day,
                prior_notice_last_time=gtfs_booking_rule.prior_notice_last_time,
                prior_notice_start_time=gtfs_booking_rule.prior_notice_start_time,
                prior_notice_calendar_id=gtfs_booking_rule.prior_notice_service_id,
                message=gtfs_booking_rule.message,
                pickup_message=gtfs_booking_rule.pickup_message,
                drop_off_message=gtfs_booking_rule.drop_off_message,
                phone_number=gtfs_booking_rule.phone_number,
                info_url=gtfs_booking_rule.info_url,
                booking_url=gtfs_booking_rule.booking_url,
            ))

    return GofsFile(FILENAME, created=True, data=booking_rules)
