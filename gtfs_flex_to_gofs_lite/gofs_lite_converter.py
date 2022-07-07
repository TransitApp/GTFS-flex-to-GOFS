import time

from .default_headers import get_default_headers
from .utils import green_text, red_text

from .files import calendars
from .files import fares
from .files import gofs
from .files import gofs_versions
from .files import operation_rules
from .files import service_brands
from .files import system_information
from .files import vehicle_types
from .files import wait_time
from .files import wait_times
from .files import zones

VERSION = '1.0'


def save_files(files, filepath, ttl, creation_timestamp):
    for file in files:
        file.save(filepath, ttl, VERSION, creation_timestamp)


def register_created_file(files_created, file):
    if not file.created:
        print('Skipped', red_text(file.get_filename_with_ext()))
        return

    print(green_text(file.get_filename_with_ext()), 'successfully created')
    files_created.append(file)


def convert_to_gofs_lite(gtfs, gofs_lite_dir, ttl, base_url):
    creation_timestamp = int(time.time())
    default_headers_template = get_default_headers(
        ttl, VERSION, creation_timestamp)

    files_created = []

    file = zones.create(gtfs)
    register_created_file(files_created, file)

    file, gofs_data = operation_rules.create(gtfs)
    register_created_file(files_created, file)

    file = system_information.create(gtfs)
    register_created_file(files_created, file)

    file = service_brands.create(gtfs, gofs_data.route_ids)
    register_created_file(files_created, file)

    file = vehicle_types.create(gtfs)
    register_created_file(files_created, file)

    file = calendars.create(gtfs, gofs_data.calendar_ids)
    register_created_file(files_created, file)

    file = fares.create(gtfs)
    register_created_file(files_created, file)

    file = wait_times.create(gtfs, gofs_data.pickup_booking_rule_ids)
    register_created_file(files_created, file)

    file = wait_time.create(gtfs)
    register_created_file(files_created, file)

    file = gofs_versions.create(default_headers_template, base_url)
    register_created_file(files_created, file)

    gofs.create(gtfs, base_url, files_created)

    save_files(files_created, gofs_lite_dir, ttl, creation_timestamp)
