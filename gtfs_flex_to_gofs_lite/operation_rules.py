from copy import deepcopy

from .default_headers import get_default_headers
from .save_file import *

FILENAME = 'operating_rules.json'

class GofsData:
    """
    Contain the different ids of data extracted from the GTFS-Flex
    Used to know what to extract in the other files
    """

    def __init__(self, used_route_ids, used_calendar_ids):
        self.route_ids = used_route_ids
        self.calendar_ids = used_calendar_ids


def get_locations_group(gtfs):
    location_groups = {}  # groupe_id -> [zone_id...]
    for group_id, group in gtfs.location_groups.items():
        location_groups.setdefault(group_id, [])
        for location in group:
            location_groups[group_id].append(location['location_id'])

    return location_groups


def get_zone_ids_set(gtfs):
    zone_ids = set()
    for zone in gtfs.locations['features']:
        zone_ids.add(zone['id'])
    return zone_ids


def create_operating_rules_file(gtfs, gofs_dir, default_headers_template):
    used_calendar_ids = set()
    used_route_ids = set()

    file = deepcopy(default_headers_template)

    operating_rules = []

    zone_ids = get_zone_ids_set(gtfs)
    locations_group = get_locations_group(gtfs)

    for stop_times in gtfs.stop_times.values():
        trip_id = stop_times[0].trip_id
        trip = gtfs.trips[trip_id]

        prev_stop_time = None
        for stop_time in stop_times:
            if prev_stop_time is not None:
                if prev_stop_time.stop_id in zone_ids and stop_time.stop_id in zone_ids:
                    # Simple Zone to Zone transfer
                    operating_rule = {
                        'from_zone_id': prev_stop_time.stop_id,
                        'to_zone_id': stop_time.stop_id,
                        'start_pickup_window': prev_stop_time.start_pickup_dropoff_window,
                        'end_pickup_window': prev_stop_time.end_pickup_dropoff_window,
                        'end_dropoff_window': '',
                        'calendars': [trip.service_id],
                        'brand_id': trip.route_id,
                        'vehicle_type_id': 'large_van'
                    }

                    used_calendar_ids.add(trip.service_id)
                    used_route_ids.add(trip.route_id)
                    operating_rules.append(operating_rule)

                elif prev_stop_time.stop_id in locations_group and stop_time.stop_id in zone_ids:
                    # Single zones to multiple zone
                    for from_stop_id in locations_group[prev_stop_time.stop_id]:
                        operating_rule = {
                            'from_zone_id': from_stop_id,
                            'to_zone_id': stop_time.stop_id,
                            'start_pickup_window': prev_stop_time.start_pickup_dropoff_window,
                            'end_pickup_window': prev_stop_time.end_pickup_dropoff_window,
                            'end_dropoff_window': '',
                            'calendars': [trip.service_id],
                            'brand_id': trip.route_id,
                            'vehicle_type_id': 'large_van'
                        }

                        used_calendar_ids.add(trip.service_id)
                        used_route_ids.add(trip.route_id)
                        operating_rules.append(operating_rule)

                elif prev_stop_time.stop_id in zone_ids and stop_time.stop_id in locations_group:
                    # Multiple zones to single zone
                    for to_stop_id in locations_group[stop_time.stop_id]:
                        operating_rule = {
                            'from_zone_id': prev_stop_time.stop_id,
                            'to_zone_id': to_stop_id,
                            'start_pickup_window': prev_stop_time.start_pickup_dropoff_window,
                            'end_pickup_window': prev_stop_time.end_pickup_dropoff_window,
                            'end_dropoff_window': '',
                            'calendars': [trip.service_id],
                            'brand_id': trip.route_id,
                            'vehicle_type_id': 'large_van'
                        }

                        used_calendar_ids.add(trip.service_id)
                        used_route_ids.add(trip.route_id)
                        operating_rules.append(operating_rule)

                elif prev_stop_time.stop_id in locations_group and stop_time.stop_id in locations_group:
                    # Multiple zones to multiple zones
                    for from_stop_id in locations_group[prev_stop_time.stop_id]:
                        for to_stop_id in locations_group[stop_time.stop_id]:
                            operating_rule = {
                                'from_zone_id': from_stop_id,
                                'to_zone_id': to_stop_id,
                                'start_pickup_window': prev_stop_time.start_pickup_dropoff_window,
                                'end_pickup_window': prev_stop_time.end_pickup_dropoff_window,
                                'end_dropoff_window': '',
                                'calendars': [trip.service_id],
                                'brand_id': trip.route_id,
                                'vehicle_type_id': 'large_van'
                            }

                            used_calendar_ids.add(trip.service_id)
                            used_route_ids.add(trip.route_id)
                            operating_rules.append(operating_rule)

            prev_stop_time = stop_time

    file['data']['operating_rules'] = operating_rules

    save_file(gofs_dir / FILENAME, file)

    return FILENAME, GofsData(used_route_ids, used_calendar_ids)
