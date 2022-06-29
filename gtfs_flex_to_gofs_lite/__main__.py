import argparse
import gtfs_loader
import json
import os
import sys
import pprint
from pathlib import Path


def get_default_headers():
    return {
        "last_updated": 1609866247,
        "ttl": 3600,
        "version": "1.0",
        "data": {}
    }


def create_gofs_file(gtfs, gofs_dir):
    file = get_default_headers()

    save_file(gofs_dir / "gofs.json", file)


def create_gofs_versions_file(gtfs, gofs_dir):
    file = get_default_headers()

    save_file(gofs_dir / "gofs_versions.json", file)


def create_system_information_file(gtfs, gofs_dir):
    file = get_default_headers()

    save_file(gofs_dir / "system_information.json", file)


def create_service_brands_file(gtfs, gofs_dir):
    file = get_default_headers()

    save_file(gofs_dir / "service_brands.json", file)


def create_vehicle_types_file(gtfs, gofs_dir):
    file = get_default_headers()

    save_file(gofs_dir / "vehicle_types.json", file)


def create_zones_file(gtfs, gofs_dir):
    file = get_default_headers()

    save_file(gofs_dir / "zones.json", file)


def create_operating_rules_file(gtfs, gofs_dir):
    file = get_default_headers()

    save_file(gofs_dir / "operating_rules.json", file)


def create_calendar_file(gtfs, gofs_dir):
    file = get_default_headers()

    save_file(gofs_dir / "calendar.json", file)


def create_fares_file(gtfs, gofs_dir):
    file = get_default_headers()

    save_file(gofs_dir / "fares.json", file)


def create_wait_times_file(gtfs, gofs_dir):
    file = get_default_headers()

    save_file(gofs_dir / "wait_times.json", file)


def create_wait_time_file(gtfs, gofs_dir):
    file = get_default_headers()

    save_file(gofs_dir / "wait_time.json", file)


def save_file(filepath, file):
    with open(filepath, 'w', encoding='utf-8-sig') as f:
        f.write(json.dumps(file, indent=4))


def main(args):
    gtfs = gtfs_loader.load(args.gtfs_dir)

    print(gtfs.locations['features'])

    for stoptimes in gtfs.stop_times.values():
        for stoptime in stoptimes:
            if stoptime.start_pickup_dropoff_window != -1:
                print("{} - {}".format(stoptime.start_pickup_dropoff_window,
                      stoptime.end_pickup_dropoff_window))

    gofs_dir = Path(args.gofs_dir)
    if not gofs_dir.exists():
        os.mkdir(gofs_dir)

    create_gofs_file(gtfs, gofs_dir)
    create_gofs_versions_file(gtfs, gofs_dir)
    create_system_information_file(gtfs, gofs_dir)
    create_service_brands_file(gtfs, gofs_dir)
    create_vehicle_types_file(gtfs, gofs_dir)
    create_zones_file(gtfs, gofs_dir)
    create_operating_rules_file(gtfs, gofs_dir)
    create_calendar_file(gtfs, gofs_dir)
    create_fares_file(gtfs, gofs_dir)
    create_wait_times_file(gtfs, gofs_dir)
    create_wait_time_file(gtfs, gofs_dir)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Convert GTFS-flex on-demand format to GOFS-lite')
    parser.add_argument(
        '--gtfs_dir', help='input gtfs directory', metavar='Dir', required=True)
    parser.add_argument(
        '--gofs_dir', help='output gofs directory', metavar='Dir', required=True)

    args = parser.parse_args()

    main(args)
