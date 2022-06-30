from copy import deepcopy

from .default_headers import get_default_headers
from .save_file import *


def create_system_information_file(gtfs, gofs_dir, default_headers_template):
    file = deepcopy(default_headers_template)

    agency = list(gtfs.agency.values())[0]

    file['data']['language'] = agency.agency_lang
    file['data']['timezone'] = agency.agency_timezone
    file['data']['name'] = agency.agency_name

    info_url = ''
    booking_url = ''
    phone_number = ''

    booking_rules = list(gtfs.booking_rule.values())
    if len(booking_rules) > 0:
        booking_rule = booking_rules[0]
        info_url = booking_rule.info_url
        booking_url = booking_rule.booking_url
        phone_number = booking_rule.phone_number

    file['data']['url'] = info_url
    file['data']['subscribe_url'] = booking_url
    file['data']['phone_number'] = phone_number

    # Fields not available in GTFS-Flex
    file['data']['short_name'] = ''
    file['data']['operator'] = ''
    file['data']['start_date'] = ''
    file['data']['email'] = ''
    file['data']['feed_contact_email'] = ''

    save_file(gofs_dir / 'system_information.json', file)
