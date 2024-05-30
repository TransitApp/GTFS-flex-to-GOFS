from dataclasses import dataclass
from typing import List

from ..gofs_file import GofsFile
from ..gofs_data import GofsData
from ..gofs_data import GofsTransfer
from gtfs_loader.schema import PickupType, DropOffType

from gtfs_flex_to_gofs_lite.utils import get_locations_group, get_zone_ids_set

FILENAME = 'operating_rules'


@dataclass
class OperationRule:
    from_zone_id: str
    to_zone_id: str
    start_pickup_window: int
    end_pickup_window: int
    end_dropoff_window: int
    calendars: List[str]
    brand_id: str
    vehicle_type_id: str


def create(gtfs):
    gofs_feed = GofsData()
    operating_rules = []

    zone_ids = get_zone_ids_set(gtfs)
    locations_group = get_locations_group(gtfs)

    for trip_id, stop_times in gtfs.stop_times.items():
        trip = gtfs.trips[trip_id]

        # Check if trip is a microtransit-like trip
        is_pure_microtransit_trip = True
        for stop_time in stop_times:
            if stop_time.start_pickup_drop_off_window == -1 or stop_time.end_pickup_drop_off_window == -1:
                is_pure_microtransit_trip = False
                break

        prev_stop_time = None
        for stop_time in stop_times:
            if prev_stop_time is None:
                prev_stop_time = stop_time
                continue

            if prev_stop_time.pickup_type == PickupType.NO_PICKUP or stop_time.drop_off_type == DropOffType.NO_DROP_OFF:
                prev_stop_time = stop_time
                continue

            from_is_valid = prev_stop_time.start_pickup_drop_off_window != -1 and prev_stop_time.end_pickup_drop_off_window != -1
            to_is_valid = stop_time.start_pickup_drop_off_window != -1 and stop_time.end_pickup_drop_off_window != -1

            if from_is_valid and to_is_valid:
                add_zone_to_zone_rule(prev_stop_time, prev_stop_time.stop_id, stop_time.stop_id, trip, operating_rules, gofs_feed)
                register_data(GofsTransfer(trip_id, prev_stop_time.stop_id, stop_time.stop_id, is_pure_microtransit_trip), trip, prev_stop_time.pickup_booking_rule_id, gofs_feed)

            continue
            if prev_stop_time.stop_id in zone_ids and stop_time.stop_id in zone_ids:
                # Single to single zone
                add_zone_to_zone_rule(prev_stop_time, prev_stop_time.stop_id,
                                      stop_time.stop_id, trip, operating_rules, gofs_feed)

                register_data(GofsTransfer(trip_id, prev_stop_time.stop_id, stop_time.stop_id, is_pure_microtransit_trip),
                              trip, prev_stop_time.pickup_booking_rule_id, gofs_feed)

            elif prev_stop_time.stop_id in locations_group and stop_time.stop_id in zone_ids:
                # Multiple zones to single zone
                for from_stop_id in locations_group[prev_stop_time.stop_id]:
                    add_zone_to_zone_rule(
                        prev_stop_time, from_stop_id, stop_time.stop_id, trip, operating_rules, gofs_feed)

                register_data(GofsTransfer(trip_id, prev_stop_time.stop_id, stop_time.stop_id, is_pure_microtransit_trip),
                              trip, prev_stop_time.pickup_booking_rule_id, gofs_feed)

            elif prev_stop_time.stop_id in zone_ids and stop_time.stop_id in locations_group:
                # Single zone to multiple zones
                for to_stop_id in locations_group[stop_time.stop_id]:
                    add_zone_to_zone_rule(prev_stop_time, prev_stop_time.stop_id, to_stop_id, trip, operating_rules, gofs_feed)

                register_data(GofsTransfer(trip_id, prev_stop_time.stop_id, stop_time.stop_id, is_pure_microtransit_trip),
                              trip, prev_stop_time.pickup_booking_rule_id, gofs_feed)

            elif prev_stop_time.stop_id in locations_group and stop_time.stop_id in locations_group:
                # Multiple zones to multiple zones
                for from_stop_id in locations_group[prev_stop_time.stop_id]:
                    for to_stop_id in locations_group[stop_time.stop_id]:
                        add_zone_to_zone_rule(
                            prev_stop_time, from_stop_id, to_stop_id, trip, operating_rules, gofs_feed)

                register_data(GofsTransfer(trip_id, prev_stop_time.stop_id, stop_time.stop_id, is_pure_microtransit_trip),
                              trip, prev_stop_time.pickup_booking_rule_id, gofs_feed)

            prev_stop_time = stop_time

    return GofsFile(FILENAME, created=True, data=operating_rules), gofs_feed


def register_data(transfer: GofsTransfer, trip, pickup_booking_rule_id, gofs_feed):
    gofs_feed.register_transfer(transfer)
    gofs_feed.register_route_id(trip.route_id)
    gofs_feed.register_calendar_id(trip.service_id)
    gofs_feed.register_pickup_booking_rule_id(pickup_booking_rule_id, transfer)


def add_zone_to_zone_rule(prev_stop_time, from_stop_id, to_stop_id, trip, operating_rules, gofs_feed):
    gofs_feed.register_zone_id(from_stop_id)
    gofs_feed.register_zone_id(to_stop_id)

    operating_rule = OperationRule(
        from_zone_id=from_stop_id,
        to_zone_id=to_stop_id,
        start_pickup_window=prev_stop_time.start_pickup_drop_off_window,
        end_pickup_window=prev_stop_time.end_pickup_drop_off_window,
        end_dropoff_window=-1,
        calendars=[trip.service_id],
        brand_id=trip.route_id,
        vehicle_type_id='large_van'
    )

    operating_rules.append(operating_rule)
