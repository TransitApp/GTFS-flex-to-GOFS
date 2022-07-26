class GofsData:
    """
    Contain the different ids of data extracted from the GTFS-Flex
    Used to know what to extract in the other files
    """

    def __init__(self):
        self.stop_ids = set()
        self.route_ids = set()
        self.calendar_ids = set()
        self.pickup_booking_rule_ids = {}

    def register_stop_id(self, stop_id):
        self.stop_ids.add(stop_id)

    def register_route_id(self, route_id):
        self.route_ids.add(route_id)

    def register_calendar_id(self, used_calendar_id):
        self.calendar_ids.add(used_calendar_id)

    def register_pickup_booking_rule_id(self, pickup_booking_rule_id, transfer):
        self.pickup_booking_rule_ids.setdefault(
            pickup_booking_rule_id, set()).add(transfer)

    def __repr__(self) -> str:
        return f'stop_ids: {repr(self.stop_ids)}\nroute_ids: {repr(self.route_ids)}\ncalendar_ids: {repr(self.calendar_ids)}\npickup_booking_rule_ids: {repr(self.pickup_booking_rule_ids)}'
