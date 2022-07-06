from copy import deepcopy

from .gofs_file import GofsFile

FILENAME = 'service_brands'


def create_service_brands_file(gtfs, route_ids):
    service_brands = []

    for route_id in route_ids:
        route = gtfs.routes[route_id]
        service_brand = {
            'brand_id': route_id,
            'brand_name': route.route_short_name if route.route_short_name != '' else route.route_long_name,
            'brand_color': route.route_color,
            'brand_text_color': route.route_text_color,
        }
        service_brands.append(service_brand)

    return GofsFile(FILENAME, True, service_brand)
