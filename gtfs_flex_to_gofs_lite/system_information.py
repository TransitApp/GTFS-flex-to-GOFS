from copy import deepcopy

from .default_headers import get_default_headers
from .gofs_file import GofsFile

FILENAME = 'system_information'


def create_system_information_file(gtfs):
    agency = list(gtfs.agency.values())[0]

    data = {}
    data['language'] = agency.agency_lang
    data['timezone'] = agency.agency_timezone
    data['name'] = agency.agency_name

    info_url = ''
    booking_url = ''
    phone_number = ''

    booking_rules = list(gtfs.booking_rules.values())
    if len(booking_rules) > 0:
        booking_rule = booking_rules[0]
        info_url = booking_rule.info_url
        booking_url = booking_rule.booking_url
        phone_number = booking_rule.phone_number

    data['url'] = info_url
    data['subscribe_url'] = booking_url
    data['phone_number'] = phone_number

    # Fields not available in GTFS-Flex
    data['short_name'] = ''
    data['operator'] = ''
    data['start_date'] = ''
    data['email'] = ''
    data['feed_contact_email'] = ''

    return GofsFile(FILENAME, True, data)
