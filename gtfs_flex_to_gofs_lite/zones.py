from copy import deepcopy

from .default_headers import get_default_headers
from .save_file import *


def create_zones_file(gtfs, gofs_dir, default_headers_template):
    file = deepcopy(default_headers_template)

    zones = {"type": "FeatureCollection", "features": []}

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

    file['data']['zones'] = zones

    save_file(gofs_dir / "zones.json", file)
