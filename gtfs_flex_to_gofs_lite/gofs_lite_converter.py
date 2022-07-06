import time

from .calendars import create_calendars_file
from .default_headers import get_default_headers
from .fares import create_fares_file
from .gofs import create_gofs_file
from .gofs_versions import create_gofs_versions_file
from .operation_rules import create_operating_rules_file
from .service_brands import create_service_brands_file
from .system_information import create_system_information_file
from .utils import GREEN_STRING, RED_STRING
from .vehicle_types import create_vehicle_types_file
from .wait_time import create_wait_time_file
from .wait_times import create_wait_times_file
from .zones import create_zones_file


VERSION = '1.0'


def save_files(files, filepath, ttl, creation_timestamp):
    for file in files:
        file.save(filepath, ttl, VERSION, creation_timestamp)


def register_created_file(files_created, file):
    if not file.created:
        print('Skipped {}'.format(RED_STRING.format(file.get_filename_with_ext())))
        return

    print('{} successfully created'.format(
        GREEN_STRING.format(file.get_filename_with_ext())))
    files_created.append(file)


def convert_to_gofs_lite(gtfs, gofs_dir, ttl, base_url):
    creation_timestamp = int(time.time())
    default_headers_template = get_default_headers(
        ttl, VERSION, creation_timestamp)

    files_created = []

    file = create_zones_file(gtfs)
    register_created_file(files_created, file)

    file, gofs_data = create_operating_rules_file(gtfs)
    register_created_file(files_created, file)

    file = create_system_information_file(gtfs)
    register_created_file(files_created, file)

    file = create_service_brands_file(gtfs, gofs_data.route_ids)
    register_created_file(files_created, file)

    file = create_vehicle_types_file(gtfs)
    register_created_file(files_created, file)

    file = create_calendars_file(gtfs, gofs_data.calendar_ids)
    register_created_file(files_created, file)

    file = create_fares_file(gtfs)
    register_created_file(files_created, file)

    file = create_wait_times_file(gtfs, gofs_data.pickup_booking_rule_ids)
    register_created_file(files_created, file)

    file = create_wait_time_file(gtfs)
    register_created_file(files_created, file)

    file = create_gofs_versions_file(default_headers_template, base_url)
    register_created_file(files_created, file)

    create_gofs_file(gtfs, base_url, files_created)

    save_files(files_created, gofs_dir, ttl, creation_timestamp)
