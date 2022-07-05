from .calendar import create_calendar_file
from .default_headers import get_default_headers
from .fares import create_fares_file
from .gofs import create_gofs_file
from .gofs_versions import create_gofs_versions_file
from .operation_rules import create_operating_rules_file
from .service_brands import create_service_brands_file
from .system_information import create_system_information_file
from .vehicle_types import create_vehicle_types_file
from .wait_time import create_wait_time_file
from .wait_times import create_wait_times_file
from .zones import create_zones_file


def convert_to_gofs_lite(gtfs, gofs_dir, ttl, base_url):
    default_headers_template = get_default_headers(ttl)

    files_created = []

    filename = create_zones_file(gtfs, gofs_dir, default_headers_template)
    if filename is not None:
        files_created.append(filename)

    filename, gofs_data = create_operating_rules_file(
        gtfs, gofs_dir, default_headers_template)
    if filename is not None:
        files_created.append(filename)

    filename = create_system_information_file(
        gtfs, gofs_dir, default_headers_template)
    if filename is not None:
        files_created.append(filename)

    filename = create_service_brands_file(
        gtfs, gofs_dir, default_headers_template, gofs_data.route_ids)
    if filename is not None:
        files_created.append(filename)

    filename = create_vehicle_types_file(
        gtfs, gofs_dir, default_headers_template)
    if filename is not None:
        files_created.append(filename)

    filename = create_calendar_file(
        gtfs, gofs_dir, default_headers_template, gofs_data.calendar_ids)
    if filename is not None:
        files_created.append(filename)

    filename = create_fares_file(gtfs, gofs_dir, default_headers_template)
    if filename is not None:
        files_created.append(filename)

    filename = create_wait_times_file(gtfs, gofs_dir, default_headers_template)
    if filename is not None:
        files_created.append(filename)

    filename = create_wait_time_file(gtfs, gofs_dir, default_headers_template)
    if filename is not None:
        files_created.append(filename)

    filename = create_gofs_versions_file(
        gtfs, gofs_dir, default_headers_template, base_url)
    if filename is not None:
        files_created.append(filename)

    create_gofs_file(gtfs, gofs_dir, default_headers_template,
                     base_url, files_created)
