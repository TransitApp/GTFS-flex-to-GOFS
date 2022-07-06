from copy import deepcopy

from .default_headers import get_default_headers
from .gofs_file import GofsFile

FILENAME = 'zones'


def create_zones_file(gtfs):
    zones = {'type': 'FeatureCollection', 'features': []}

    for zone in gtfs.locations['features']:
        new_zone = {
            'type': 'Feature',
            'zone_id': zone['id'],
            'properties': {
                'name': zone['properties'].get('stop_name', '')
                # Unused GTFS-flex field
                # zone['properties'].get('stop_desc', '')
                # zone['properties'].get('zone_id', '')
                # zone['properties'].get('stop_url', '')
            },
            'geometry': zone['geometry']
        }

        zones['features'].append(new_zone)

    return GofsFile(FILENAME, True, zones)
