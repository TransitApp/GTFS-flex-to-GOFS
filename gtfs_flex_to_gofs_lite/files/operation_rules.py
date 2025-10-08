from dataclasses import dataclass
from typing import List

from ..gofs_file import GofsFile
from ..gofs_data import GofsData
from ..gofs_data import GofsTransfer
from gtfs_loader.schema import PickupType, DropOffType

from gtfs_flex_to_gofs_lite.utils import get_locations_group, get_zones
from enum import Enum

FILENAME = 'operating_rules'

class TripType(Enum):
    REGULAR_SERVICE = "regular_service"
    DEVIATED_SERVICE = "deviated_service"
    PURE_MICROTRANSIT = "pure_microtransit"
    OTHER = "other"

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


def create(gtfs, itineraries=False):
    gofs_feed = GofsData()
    operating_rules = []

    if itineraries:
        for trip in gtfs.trips.values():
            # Check if trip is a microtransit-like trip
            type_of_trip = get_type_of_itinerary_trip(trip)
            if type_of_trip == TripType.PURE_MICROTRANSIT:
                itin_cells = gtfs.itinerary_cells[trip.itinerary_index].values()
                prev_itin_cell = None
                for i, itin_cell in enumerate(itin_cells):
                    if prev_itin_cell is None:
                        prev_itin_cell = itin_cell
                        continue

                    if prev_itin_cell.pickup_type == PickupType.NO_PICKUP or prev_itin_cell.drop_off_type == DropOffType.NO_DROP_OFF:
                        prev_itin_cell = itin_cell
                        continue

                    from_is_valid = trip.start_pickup_drop_off_windows[i - 1] != -1 and trip.end_pickup_drop_off_windows[i - 1] != -1
                    to_is_valid = trip.start_pickup_drop_off_windows[i] != -1 and trip.end_pickup_drop_off_windows[i] != -1

                    if from_is_valid and to_is_valid:
                        add_zone_to_zone_rule(trip.start_pickup_drop_off_windows[i - 1], trip.end_pickup_drop_off_windows[i - 1], prev_itin_cell.stop_id, itin_cell.stop_id, trip, operating_rules, gofs_feed)
                        register_data(GofsTransfer(trip.trip_id, prev_itin_cell.stop_id, prev_itin_cell.stop_id), trip, prev_itin_cell.pickup_booking_rule_id, gofs_feed)
                    

    else:
        for trip_id, stop_times in gtfs.stop_times.items():
            trip = gtfs.trips[trip_id]

            # Check if trip is a microtransit-like trip
            type_of_trip = get_type_of_trip(stop_times)

            if type_of_trip == TripType.PURE_MICROTRANSIT:
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
                        add_zone_to_zone_rule(prev_stop_time.start_pickup_drop_off_window, prev_stop_time.end_pickup_drop_off_window, prev_stop_time.stop_id, stop_time.stop_id, trip, operating_rules, gofs_feed)
                        register_data(GofsTransfer(trip_id, prev_stop_time.stop_id, stop_time.stop_id), trip, prev_stop_time.pickup_booking_rule_id, gofs_feed)
                    

    operating_rules.sort(key=lambda x: (x.from_zone_id, x.to_zone_id, x.brand_id, x.vehicle_type_id, x.start_pickup_window, x.end_pickup_window, x.end_dropoff_window, x.calendars))

    return GofsFile(FILENAME, created=True, data=operating_rules), gofs_feed

class StopType(Enum):
    REGION = "region"
    STOP = "stop"

def get_type_of_trip(stop_times):
    # Invalid trips with fewer than 2 stops are marked as OTHER
    if len(stop_times) < 2:
        return TripType.OTHER

    # Find which trips should be kept in GTFS
    # By default, we don't keep it because we assume it's a microtransit trip
    # If we have a deviated services, keep it (at least two stops and one region in the middle) 
    # if it's a regular service, we keep it
    regular_service = True
    microtransit_only = True
    deviated_service = len(stop_times) > 2 # at least 3 stop times, otherwise it's not a deviated service
    previous_stop_type = None

    for stop_time in stop_times:
        is_a_region = stop_time.start_pickup_drop_off_window != -1 or stop_time.end_pickup_drop_off_window != -1

        if is_a_region:
            regular_service = False # either deviated or microtransit only
        else:
            microtransit_only = False
        
        if previous_stop_type == StopType.REGION and is_a_region:
            deviated_service = False
        
        previous_stop_type = StopType.REGION if is_a_region else StopType.STOP

    if regular_service:
        return TripType.REGULAR_SERVICE
    elif deviated_service:
        return TripType.DEVIATED_SERVICE
    elif microtransit_only:
        return TripType.PURE_MICROTRANSIT 
    else:
        return TripType.OTHER

def get_type_of_itinerary_trip(trip):
    # Invalid trips with fewer than 2 stops are marked as OTHER
    if len(trip.start_pickup_drop_off_windows) < 2:
        return TripType.OTHER

    # Find which trips should be kept in GTFS
    # By default, we don't keep it because we assume it's a microtransit trip
    # If we have a deviated services, keep it (at least two stops and one region in the middle) 
    # if it's a regular service, we keep it
    regular_service = True
    microtransit_only = True
    deviated_service = len(trip.start_pickup_drop_off_windows) > 2 # at least 3 stop times, otherwise it's not a deviated service
    previous_stop_type = None

    for i, start_pickup_drop_off_window in enumerate(trip.start_pickup_drop_off_windows):
        is_a_region = start_pickup_drop_off_window != -1 or trip.end_pickup_drop_off_windows[i] != -1

        if is_a_region:
            regular_service = False # either deviated or microtransit only
        else:
            microtransit_only = False
        
        if previous_stop_type == StopType.REGION and is_a_region:
            deviated_service = False
        
        previous_stop_type = StopType.REGION if is_a_region else StopType.STOP

    if regular_service:
        return TripType.REGULAR_SERVICE
    elif deviated_service:
        return TripType.DEVIATED_SERVICE
    elif microtransit_only:
        return TripType.PURE_MICROTRANSIT 
    else:
        return TripType.OTHER  


def register_data(transfer: GofsTransfer, trip, pickup_booking_rule_id, gofs_feed):
    gofs_feed.register_transfer(transfer)
    gofs_feed.register_route_id(trip.route_id)
    gofs_feed.register_calendar_id(trip.service_id)
    gofs_feed.register_pickup_booking_rule_id(pickup_booking_rule_id, transfer)


def add_zone_to_zone_rule(prev_start_pickup_window, prev_end_pickup_window, from_stop_id, to_stop_id, trip, operating_rules, gofs_feed):
    gofs_feed.register_zone_id(from_stop_id)
    gofs_feed.register_zone_id(to_stop_id)

    operating_rule = OperationRule(
        from_zone_id=from_stop_id,
        to_zone_id=to_stop_id,
        start_pickup_window=prev_start_pickup_window,
        end_pickup_window=prev_end_pickup_window,
        end_dropoff_window=-1,
        calendars=[trip.service_id],
        brand_id=trip.route_id,
        vehicle_type_id='large_van'
    )

    operating_rules.append(operating_rule)
