import time


def get_default_headers(ttl):
    return {
        'last_updated': int(time.time()),
        'ttl': ttl,
        'version': '1.0',
        'data': {}
    }
