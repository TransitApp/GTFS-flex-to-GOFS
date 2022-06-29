from tracemalloc import stop
from .default_headers import get_default_headers
from .save_file import *

def get_zone_ids_set(gtfs):
    zone_ids = set()
    for zone in gtfs.locations['features']:
        zone_ids.add(zone['id'])
    return zone_ids

def create_operating_rules_file(gtfs, gofs_dir):
    file = get_default_headers(gtfs)

    operating_rules = []

    zone_ids = get_zone_ids_set(gtfs)
    
    for stop_times in gtfs.stop_times.values():
        prev_stop_time = None
        for stop_time in stop_times:

            if prev_stop_time is not None and prev_stop_time.stop_id in zone_ids and stop_time.stop_id in zone_ids:
                operating_rule = {
                        "from_zone_id": prev_stop_time.stop_id,
                        "to_zone_id": stop_time.stop_id,
                        "start_pickup_window" : prev_stop_time.start_pickup_dropoff_window,
                        "end_pickup_window": prev_stop_time.end_pickup_dropoff_window,
                        "end_dropoff_window": "09:30:00",
                        "calendars": ["weekend", "labor_day"],
                        "brand_id": "large_ride",
                        "vehicle_type_id": "large_van"
                    }

                operating_rules.append(operating_rule)

            prev_stop_time = stop_time

    file['data']['operating_rules'] = operating_rules

    save_file(gofs_dir / "operating_rules.json", file)