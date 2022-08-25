from dataclasses import dataclass
from typing import Any, List

from gtfs_flex_to_gofs_lite.gofs_data import GofsData

from ..gofs_file import GofsFile

FILENAME = 'zones'


@dataclass
class Properties:
    name: str


@dataclass
class Feature:
    zone_id: str
    properties: Properties
    geometry: Any
    type: str = 'Feature'


@dataclass
class Zones:
    features: List[Feature]
    type: str = 'FeatureCollection'


def create(gtfs, gofs_data: GofsData):
    zones = []

    for zone in gtfs.locations['features']:

        if zone['id'] not in gofs_data.zones_ids:
            continue

        new_zone = Feature(
            zone_id=zone['id'],
            properties=Properties(
                name=zone['properties'].get('stop_name', '')
                # Unused GTFS-flex field
                # zone['properties'].get('stop_desc', '')
                # zone['properties'].get('zone_id', '')
                # zone['properties'].get('stop_url', '')
            ),
            geometry=zone['geometry']
        )

        zones.append(new_zone)

    return GofsFile(FILENAME, created=True, data=Zones(zones))
