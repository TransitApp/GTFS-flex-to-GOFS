from gtfs_flex_to_gofs.files.operation_rules import add_zone_to_zone_rule, OperationRule
from gtfs_flex_to_gofs.gofs_data import GofsData


class MockStopTime:
    def __init__(self, start_window, end_window):
        self.start_pickup_drop_off_window = start_window
        self.end_pickup_drop_off_window = end_window


class MockTrip:
    def __init__(self, service_id, route_id):
        self.service_id = service_id
        self.route_id = route_id


def test_rules_with_same_key_merge_calendars():
    rules_by_key = {}
    gofs_feed = GofsData()
    stop_time = MockStopTime(100, 200)

    add_zone_to_zone_rule(stop_time, "zone_a", "zone_b", MockTrip("cal_1", "route_1"), rules_by_key, gofs_feed)
    add_zone_to_zone_rule(stop_time, "zone_a", "zone_b", MockTrip("cal_2", "route_1"), rules_by_key, gofs_feed)
    add_zone_to_zone_rule(stop_time, "zone_a", "zone_b", MockTrip("cal_3", "route_1"), rules_by_key, gofs_feed)

    assert len(rules_by_key) == 1
    rule = list(rules_by_key.values())[0]
    assert sorted(rule.calendars) == ["cal_1", "cal_2", "cal_3"]


def test_duplicate_calendar_not_added_twice():
    rules_by_key = {}
    gofs_feed = GofsData()
    stop_time = MockStopTime(100, 200)

    add_zone_to_zone_rule(stop_time, "zone_a", "zone_b", MockTrip("cal_1", "route_1"), rules_by_key, gofs_feed)
    add_zone_to_zone_rule(stop_time, "zone_a", "zone_b", MockTrip("cal_1", "route_1"), rules_by_key, gofs_feed)

    assert len(rules_by_key) == 1
    assert list(rules_by_key.values())[0].calendars == {"cal_1"}


def test_different_zones_create_separate_rules():
    rules_by_key = {}
    gofs_feed = GofsData()
    stop_time = MockStopTime(100, 200)

    add_zone_to_zone_rule(stop_time, "zone_a", "zone_b", MockTrip("cal_1", "route_1"), rules_by_key, gofs_feed)
    add_zone_to_zone_rule(stop_time, "zone_a", "zone_c", MockTrip("cal_1", "route_1"), rules_by_key, gofs_feed)

    assert len(rules_by_key) == 2


def test_different_time_windows_create_separate_rules():
    rules_by_key = {}
    gofs_feed = GofsData()

    add_zone_to_zone_rule(MockStopTime(100, 200), "zone_a", "zone_b", MockTrip("cal_1", "route_1"), rules_by_key, gofs_feed)
    add_zone_to_zone_rule(MockStopTime(300, 400), "zone_a", "zone_b", MockTrip("cal_1", "route_1"), rules_by_key, gofs_feed)

    assert len(rules_by_key) == 2


def test_different_routes_create_separate_rules():
    rules_by_key = {}
    gofs_feed = GofsData()
    stop_time = MockStopTime(100, 200)

    add_zone_to_zone_rule(stop_time, "zone_a", "zone_b", MockTrip("cal_1", "route_1"), rules_by_key, gofs_feed)
    add_zone_to_zone_rule(stop_time, "zone_a", "zone_b", MockTrip("cal_1", "route_2"), rules_by_key, gofs_feed)

    assert len(rules_by_key) == 2
