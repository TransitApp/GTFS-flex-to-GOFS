import argparse
from copy import deepcopy
import gtfs_loader
import json
import os
from pathlib import Path

from .calendar import create_calendar_file
from .default_headers import get_default_headers
from .gofs import create_gofs_file
from .operation_rules import create_operating_rules_file
from .system_information import create_system_information_file
from .zones import create_zones_file

DEFAULT_TTL = 86400


def create_gofs_versions_file(gtfs, gofs_dir, default_headers_template):
    file = deepcopy(default_headers_template)

    save_file(gofs_dir / "gofs_versions.json", file)


def create_service_brands_file(gtfs, gofs_dir, default_headers_template):
    file = deepcopy(default_headers_template)

    save_file(gofs_dir / "service_brands.json", file)


def create_vehicle_types_file(gtfs, gofs_dir, default_headers_template):
    file = deepcopy(default_headers_template)

    save_file(gofs_dir / "vehicle_types.json", file)


def create_fares_file(gtfs, gofs_dir, default_headers_template):
    file = deepcopy(default_headers_template)

    save_file(gofs_dir / "fares.json", file)


def create_wait_times_file(gtfs, gofs_dir, default_headers_template):
    file = deepcopy(default_headers_template)

    save_file(gofs_dir / "wait_times.json", file)


def create_wait_time_file(gtfs, gofs_dir, default_headers_template):
    file = deepcopy(default_headers_template)

    save_file(gofs_dir / "wait_time.json", file)


def save_file(filepath, file):
    with open(filepath, 'w', encoding='utf-8-sig') as f:
        f.write(json.dumps(file, indent=4))


def main(args):
    gtfs = gtfs_loader.load(args.gtfs_dir)
    gofs_dir = Path(args.gofs_dir)
    ttl = args.ttl

    if not gofs_dir.exists():
        os.mkdir(gofs_dir)

    default_headers_template = get_default_headers(args.ttl)

    create_gofs_file(gtfs, gofs_dir, default_headers_template)

    create_gofs_versions_file(gtfs, gofs_dir, default_headers_template)

    create_system_information_file(gtfs, gofs_dir, default_headers_template)

    create_service_brands_file(gtfs, gofs_dir, default_headers_template)

    create_vehicle_types_file(gtfs, gofs_dir, default_headers_template)

    create_zones_file(gtfs, gofs_dir, default_headers_template)

    used_calendar_ids = create_operating_rules_file(
        gtfs, gofs_dir, default_headers_template)

    create_calendar_file(
        gtfs, gofs_dir, default_headers_template, used_calendar_ids)

    create_fares_file(gtfs, gofs_dir, default_headers_template)

    create_wait_times_file(gtfs, gofs_dir, default_headers_template)

    create_wait_time_file(gtfs, gofs_dir, default_headers_template)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Convert GTFS-flex on-demand format to GOFS-lite')
    parser.add_argument(
        '--gtfs_dir', help='input gtfs directory', metavar='Dir', required=True)
    parser.add_argument(
        '--gofs_dir', help='output gofs directory', metavar='Dir', required=True)
    parser.add_argument(
        '--ttl', help='time to live of the generated gofs files in seconds (default: 86400)', type=int, default=DEFAULT_TTL)

    args = parser.parse_args()

    main(args)
