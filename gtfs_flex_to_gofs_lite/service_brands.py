from copy import deepcopy

from .default_headers import get_default_headers
from .save_file import *


def create_service_brands_file(gtfs, gofs_dir, default_headers_template, route_ids):
    file = deepcopy(default_headers_template)

    service_brands = []

    for route_id in route_ids:
        route = gtfs.routes[route_id]
        service_brand = {
            "brand_id": route_id,
            "brand_name": route.route_short_name if route.route_short_name != '' else route.route_long_name,
            "brand_color": route.route_color,
            "brand_text_color": route.route_text_color,
        }
        service_brands.append(service_brand)

    file['data']['service_brands'] = service_brands

    save_file(gofs_dir / "service_brands.json", file)
